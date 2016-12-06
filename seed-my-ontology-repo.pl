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
my $skip_install = 0;
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
    elsif ($opt eq '-s' || $opt eq '--skip-install') {
        $skip_install = 1;
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
my $ontid = shift @ARGV;
if (!$ontid) {
    die "MUST SPECIFY AN ONTOLOGY ID.\nRun script with -h for details";
}
$ontid = lc($ontid);

my $prefix = uc($ontid);


if ($clean) {
    `rm -rf target`;
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


my $TEMPLATEDIR = 'template';

my @files;
finddepth(sub {
    return if($_ eq '.' || $_ eq '..');
    push @files, $File::Find::name;
          }, 
          $TEMPLATEDIR
    );
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

install() unless $skip_install;
## NOTE: all ops in this dir from now on
chdir($targetdir);

runcmd("git init");
runcmd("git add -A .");
runcmd("git commit -m 'initial commit of ontology sources of $ontid using ontology-starter-kit' -a") unless $no_commit;

runcmd("mkdir bin") unless -d "bin";
runcmd("cp ../../bin/* bin/");
$ENV{PATH} = "$ENV{PATH}:$ENV{PWD}/bin";

if ($n_errors) {
    print STDERR "WARNING: encountered errors - the commands below may not work\n";
}

if ($prep_initial_release) {
    print STDERR "Preparing initial release, may take a few minutes, or longer if you depend on large ontologies like chebi\n";
    my $cmd = "cd src/ontology && make prepare_release && echo SUCCESS || echo FAILURE";
    runcmd($cmd);
    
    runcmd("git add src/ontology/imports/*{obo,owl}") if @depends;
    runcmd("git add src/ontology/subsets/*{obo,owl}") if -d "src/ontology/subsets";
    runcmd("git add $ontid.{obo,owl}");
    runcmd("git add imports/*{obo,owl}") if @depends;
    runcmd("git add subsets/*{obo,owl}") if -d "src/ontology/subsets";
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

sub install {
    return if -f "bin/apply-pattern.py";
    runcmd("mkdir bin") unless -d "bin";
    runcmd("wget http://build.berkeleybop.org/userContent/owltools/owltools -O bin/owltools") unless -f "bin/owltools";
    runcmd("wget http://build.berkeleybop.org/userContent/owltools/ontology-release-runner -O bin/ontology-release-runner") unless -f "bin/ontology-release-runner";
    runcmd("wget http://build.berkeleybop.org/userContent/owltools/owltools-runner-all.jar -O bin/owltools-runner-all.jar") unless -f "owltools-runner-all.jar";
    runcmd("wget http://build.berkeleybop.org/userContent/owltools/owltools-oort-all.jar -O bin/owltools-oort-all.jar") unless -f "owltools-oort-all.jar";
    runcmd("wget http://build.berkeleybop.org/job/robot/lastSuccessfulBuild/artifact/bin/robot -O bin/robot");
    runcmd("wget http://build.berkeleybop.org/job/robot/lastSuccessfulBuild/artifact/bin/robot.jar -O bin/robot.jar") unless -f "bin/robot.jar";
    runcmd("wget --no-check-certificate https://raw.githubusercontent.com/cmungall/pattern2owl/master/apply-pattern.py -O bin/apply-pattern.py");
    runcmd("chmod +x bin/*");

}

sub runcmd {
    my $cmd = shift;
    print "EXECUTING: $cmd\n";
    my $err = system($cmd);
    if ($err) {
        print STDERR "ERROR RUNNING: $cmd\n";
        $n_errors ++;
        if (!$force) {
            die "Exiting. Run with '-f' to force execution and ignore errors";
        }
    }
    #print `$cmd`;
}

sub copy_template {
    my $f = shift;
    my $tf = shift;
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
}

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

EOM
}

