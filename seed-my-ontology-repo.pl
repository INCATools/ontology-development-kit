#!/usr/bin/perl -w

use strict;
use File::Find qw(finddepth);
use File::Basename;

my $n_errors = 0;


my @depends = ();
my $org = "obophenotype";
my $title;
my $clean = 0;
my $prep_initial_release = 1;
my $no_commit = 0;
my $force = 0;
my $use_docker = 0;
my $email = "";
my $interactive = 0;


print '           ._____     '; print "\n";
print '  ____   __| _/  | __ '; print "\n";
print ' /  _ \ / __ ||  |/ / '; print "\n";
print '(  <_> ) /_/ ||    <  '; print "\n";
print ' \____/\____ ||__|_ \ '; print "\n";
print '            \/     \/ '; print "\n";


print "Welcome to the ontology development kit repository creator!\n";
print "For full instructions, see https://github.com/INCATools/ontology-development-kit!\n\n";

print "ARGUMENTS: [ @ARGV ]\n";

if (scalar(@ARGV) == 0) {
    print "No arguments specified: entering interactive mode\n";
    print "If this is not your intention, answer \"!\" to any question to quit.\n";
    print "Run with -h option for help.\n\n";
    $interactive = 1;
}

while (scalar(@ARGV) && $ARGV[0] =~ /^\-/) {
    my $opt = shift @ARGV;
    if ($opt eq '-h' || $opt eq '--help') {
        print usage();
        exit 0;
    }
    elsif ($opt eq '-d' || $opt eq '--depends') {
        while (scalar(@ARGV) && $ARGV[0] !~ m@^\-@) {
            push(@depends, shift @ARGV);
        }
    }
    elsif ($opt eq '-u' || $opt eq '--user') {
        $org = shift @ARGV;
    }
    elsif ($opt eq '-t' || $opt eq '--title') {
        $title = shift @ARGV;
    }
    elsif ($opt eq '-c' || $opt eq '--clean') {
        $clean = 1;
    }
    elsif ($opt eq '-f' || $opt eq '--force') {
        $force = 1;
    }
    elsif ($opt eq '-D' || $opt eq '--use-docker') {
        $use_docker = 1;
    }
    elsif ($opt eq '-I' || $opt eq '--interactive') {
        $interactive = 1;
    }
    elsif ($opt eq '-e' || $opt eq '--email') {
        $email = shift @ARGV;
    }
    elsif ($opt eq '--no-release') {
        $prep_initial_release = 0;
    }
    elsif ($opt eq '--no-commit') {
        $no_commit = 1;
    }
    elsif ($opt eq '-') {
    }
    else {
        die "$opt";
    }
}

my $ontid;

if ($interactive || (!scalar(@ARGV) && !$title)) {
    print "================\n";
    print "INTERACTIVE MODE\n";
    print "================\n";
    print "\nEnter '!' as answer to quit and start again\n\n";
    question(\$ontid,
             "ontid",
             "What is the OBO ontology ID / ID prefix of your ontology?",
             "For example: mp, go, triffo.\nNote that the ID prefix will be auto-capitalized");
    question(\$title,
             "title",
             "What is the name/title of your ontology?",
             "For example: triffid behavior ontology.\nTwo to three words recommended. This will be used to derive the github repository name");
    question(\@depends,
             "dependencies",
             "What ontologies should be used to make imports (separate list with spaces)?",
             "For example: 'ro po envo'.\nSee obofoundry.org for a list of ontology ids");
    question(\$org,
             "org",
             "What is the github oranization or username?",
             "For example: obophenotype, cmungall, geneontology.");
}
else {
    $ontid = shift @ARGV;
    if (!$ontid) {
        die "MUST SPECIFY AN ONTOLOGY ID.\nRun script with -h for details";
    }
}

$ontid = lc($ontid);

my $prefix = uc($ontid);

if (!@depends) {
    print STDERR "You MUST specify at least one dependency to build an OBO ontology.\n";
    print STDERR "Note that new dependencies can be added later.\n";
    print STDERR "If you are unsure, just use 'ro'. This can be specified with the -d option, or in interactive mode.\n";
    exit 1;
}

if ($clean) {
    `rm -rf target/*`;
}

if (!$title) {
    $title = $ontid;
}
my $depends_str = join(" ", @depends);


my $targetdir = lc($title);

$targetdir =~ s/\W/-/g;
$targetdir =~ s/_/-/g;
$targetdir =~ tr/a-z\-//cd;

my $repo_name = $targetdir;

$targetdir = "target/$targetdir";
mkdir("target") unless -d 'target';
mkdir("$targetdir") unless -d $targetdir;

if (-d "$targetdir/.git") {
    print STDERR "It looks like there is a previous attempt here: $targetdir/.git\n";
    print STDERR "I recommend blowing away and starting again using the '-c' option to clean\n";
    die;
}

if ($email eq "") {
    #print STDERR "Must supply email address with -e|--email <email>\n";
}
else {
    runcmd("git config --global user.name $org");
    runcmd("git config --global user.email $email");
}

my $TEMPLATEDIR = 'template';

my @files;
#finddepth(sub {
#    return if($_ eq '.' || $_ eq '..');
#    push @files, $File::Find::name;
#},
#$TEMPLATEDIR
#);

my @dirs = ($TEMPLATEDIR);

while (@dirs) {
    my $thisdir = shift @dirs;
    my $dh;
	opendir $dh, $thisdir;
	while (my $entry = readdir $dh) {
		next if $entry eq '.';
		next if $entry eq '..';

		my $fullname = "$thisdir/$entry";
		print "FOUND: $fullname \n";

		if (-d $fullname) {
			push @dirs, $fullname;
		} else {
			push @files, $fullname;
		}
	}
}

#push(@files, "$TEMPLATEDIR/.gitignore");

while (my $f = shift @files) {
    if (-d $f) {
        next;
    }
    $f =~ s@^$TEMPLATEDIR/@@;
    next if $f eq 'git';
    my $tf = $f;
    if ($f =~ /foobar/) {
        $tf = replace($f);
    }
    $tf = "$targetdir/$tf";
    if ($tf =~ m@MY-IMPORTED@) {
        # special case: if the filename has MY-IMPORTED in it,
        # use this as a template to make one file for each ontology dependency
        foreach my $depend (@depends) {
            $_ = $tf;
            s@MY-IMPORTED@$depend@;
            copy_template($f, $_);

        }
    }
    else {
        copy_template($f, $tf);
    }
}


## NOTE: all ops in this dir from now on
chdir($targetdir);

runcmd("git init");
runcmd("git add -A .");
runcmd("git commit -m 'initial commit of ontology sources of $ontid using ontology-starter-kit' -a") unless $no_commit;

if ($n_errors) {
    print STDERR "WARNING: encountered errors - the commands below may not work\n";
}

if ($prep_initial_release) {
    print STDERR "Preparing initial release, may take a few minutes, or longer if you depend on large ontologies like chebi\n";
    my $MAKE = "make prepare_release";
    if ($use_docker) {
        $MAKE = "./run.sh $MAKE";
    }
    #my $cmd = "cd src/ontology && $MAKE && echo SUCCESS || echo FAILURE";
    my $cmd = "cd src/ontology && $MAKE";
    runcmd($cmd);

    runcmd("git add src/ontology/imports/*.{obo,owl}") if @depends;
    runcmd("git add src/ontology/imports/*.{obo,owl}") if @depends;
    runcmd("git add src/ontology/subsets/*.{obo,owl}") if -d "src/ontology/subsets";
    runcmd("git add $ontid.{obo,owl}");
    runcmd("git add imports/*.{obo,owl}") if @depends;
    runcmd("git add subsets/*.{obo,owl}") if -d "src/ontology/subsets";
    runcmd("git commit -m 'initial release of $ontid using ontology-starter-kit' -a") unless $no_commit;
}

runcmd("git status");



print "\n\n####\nNEXT STEPS:\n";
print " 0. Examine $targetdir and check it meets your expectations. If not blow it away and start again\n";
print " 1. Go to: https://github.com/new\n";
print " 2. The owner MUST be $org. The Repository name MUST be $repo_name\n";
print " 3. Do not initialize with a README (you already have one)\n";
print " 4. Click Create\n";
print " 5. See the section under '…or push an existing repository from the command line'\n";
print "    E.g.:\n";
print "cd $targetdir\n";
print "git remote add origin git\@github.com:$org/$repo_name.git\n";
print "git push -u origin master\n\n";
print "BE BOLD: you can always delete your repo and start again\n\n";
print "\n";
print "FINAL STEPS:\n";
print "Folow your customized instructions here:\n\n";
print "    https://github.com/$org/$repo_name/blob/master/src/ontology/README-editors.md\n";
print "\n";


exit 0;

sub question {
    my ($varref, $short, $question, $info) = @_;
    print "\n$question\n$info\n:: $short > ";
    my $answered = 0;
    while (!$answered) {
        my $answer = <STDIN>;
        chomp $answer;
        $answer =~ s@^\s+@@;
        $answer =~ s@\s+$@@;

        if ($answer =~ m@\!@) {
            print "QUITTING\n";
            exit 1;
        }
        
        if (ref $varref eq 'ARRAY') {
            @$varref = split(' ', $answer);
        }
        else {
            $$varref = $answer;
        }
        if ($answer) {
            print " * $short=\"$answer\"\n";
            $answered = 1;
        }
    }
}

sub runcmd {
    my $cmd = shift;
    my $exit_on_fail = shift;
    print "EXECUTING: $cmd\n";

    # not all shells support {...} syntax
    # we auto-unfold these here
    # see https://github.com/INCATools/ontology-starter-kit/pull/49
    if ($cmd =~ m@(.*)\{(.*)\}(.*)@) {
        my ($pre, $matchlist, $post) = ($1,$2,$3);
        my @expansions = split(/,/, $matchlist);
        print "Expanded: $matchlist => @expansions\n";
        foreach (@expansions) {
            runcmd("$pre$_$post", $exit_on_fail);
        }
        return;
    }
    my $err = system($cmd);
    if ($err) {
        print STDERR "ERROR RUNNING: $cmd\n";
        $n_errors ++;
        if (!$force || $exit_on_fail) {
            die "Exiting. Run with '-f' to force execution and ignore errors";
        }
    }
    #print `$cmd`;
}

sub copy_template {
    my $f = shift;   ## source file
    my $tf = shift;  ## target file
    open(F, "$TEMPLATEDIR/$f") || die $f;
    recursive_mkdir($tf);
    print STDERR "WRITING: $tf\n";
    open(OF, ">$tf") || die $tf;
    while(<F>) {
        if (m@MY-IMPORTED@) {
            my $orig = $_;
            foreach my $depend (@depends) {
                $_ = $orig;
                s@MY-IMPORTED@$depend@g;
                print OF replace($_);
            }
        }
        else {
            print OF replace($_);
        }
    }
    close(OF);
    close(F);
    if ($tf =~ m@\.sh$@) {
        runcmd("chmod +x $tf");
    }
}

# replace variable names in template with variable values
sub replace {
    my $s = shift;
    $s =~ s/foobar/$ontid/g;
    $s =~ s/FOOBAR/$prefix/g;
    $s =~ s/MY_IMPORTS_LIST/$depends_str/g;
    $s =~ s/MY-ONTOLOGY-TITLE/$title/g;
    $s =~ s/MY-GITHUB-ORG/$org/g;
    $s =~ s/MY-REPO-NAME/$repo_name/g;
    return $s;
}

sub scriptname {
    my @p = split(/\//,$0);
    pop @p;
}

sub recursive_mkdir {
    my $path = shift;
    my @parts = split(/\//, $path);
    pop @parts; ## just use dirname, not file
    my @d = ();
    while (my $part = shift @parts) {
        push(@d, $part);
        my $dn = join("/",@d);
        mkdir($dn) unless -d $dn;
    }
}

sub usage {
    my $sn = scriptname();

    <<EOM;
    $sn [-d IMPORTED-ONTOLOGY-ID]* [-u GITHUB-USER-OR-ORG] [-t TITLE] [-c] ONTOLOGY-ID

    Generates an ontology repo from templates, into the target/ directory

    Example:

    $sn  -d po -d ro -d pato -u obophenotype -t "Triffid Behavior ontology" triffo

    See http://github.com/cmungall/ontology-starter-kit for details

    Options:

    -d ONT1 ONT2 ... : a list of ontology IDs that will form the import modules
    -u USER_OR_ORG   : a GitHub username or organization.
    -t TITLE         : a descriptive name for your ontology, e.g "Sloth Behavior Ontology"
    -c               : make a clean version
    --no-commit      : do not run the commit operation

    Note the title is used to determine the repo/folder name, e.g. sloth-behavior-ontology

EOM
}
