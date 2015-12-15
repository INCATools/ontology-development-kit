#!/usr/bin/perl -w

use strict;
use File::Find qw(finddepth);
use File::Basename;

my @depends = ();
my $org = "obophenotype";
my $title;
my $clean = 0;
my $prep_initial_release = 1;
my $no_commit = 0;
while (scalar(@ARGV) && $ARGV[0] =~ /^\-/) {
    my $opt = shift @ARGV;
    if ($opt eq '-h' || $opt eq '--help') {
        print usage();
        exit 0;
    }
    elsif ($opt eq '-d' || $opt eq '--depends') {
        push(@depends, shift @ARGV);
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
my $ontid = lc(shift @ARGV);
my $prefix = uc($ontid);

if (!$ontid) {
    die "MUST SPECIFY AN ONTOLOGY ID. Run with -h for details";
}

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

while (my $f = shift @files) {
    if (-d $f) {
        next;
    }
    $f =~ s@^$TEMPLATEDIR/@@;
    next if $f =~ m@^\.git@;
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

## NOTE: all ops in this dir from now on
chdir($targetdir);

runcmd("git init");
runcmd("git add -A .");
runcmd("git commit -m 'initial commit of ontology sources of $ontid using ontology-starter-kit' -a") unless $no_commit;


if ($prep_initial_release) {
    print STDERR "Preparing initial release, may take a few minutes, or longer if you depend on large ontologies like chebi\n";
    my $cmd = "cd src/ontology && make prepare_release && echo SUCCESS || echo FAILURE";
    runcmd($cmd);
    
    runcmd("git add src/ontology/imports/*{obo,owl}");
    runcmd("git add src/ontology/subsets/*{obo,owl}");
    runcmd("git add *{obo,owl}");
    runcmd("git add imports/*{obo,owl}");
    runcmd("git add subsets/*{obo,owl}");
    runcmd("git commit -m 'initial release of $ontid using ontology-starter-kit' -a") unless $no_commit;
}

runcmd("git status");

print "NEXT STEPS:\n";
print " 0. Example $targetdir and check it meets your expectations. If not blow it away and start again\n";
print " 1. Go to: https://github.com/new\n";
print " 2. The owner MUST be $org. The Repository name MUST be $title\n";
print " 3. Do not initialize with a README (you already have one)\n";
print " 4. Click Create\n";
print " 5. See the section under '…or push an existing repository from the command line'\n";
print "    E.g.:\n";
print "cd $targetdir\n";
print "git remote add origin git\@github.com:$org/$ontid.git\n";
print "git push -u origin master\n\n";
print "BE BOLD: you can always delete your repo and start again\n\n";


exit 0;

sub runcmd {
    my $cmd = shift;
    print "EXECUTING: $cmd\n";
    print `$cmd`;
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

Generates an ontology repo from templates. Will be built in target/ONTOLOGY-ID

Example:

$sn  -d chebi -d ro -u obophenotype -t "ontology-of-foos-and-bars" foobaro

See http://github.com/cmungall/ontology-starter-kit for details

EOM
}

