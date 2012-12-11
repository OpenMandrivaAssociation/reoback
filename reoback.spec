%define srcver 1.0_r3
%define tarver 1.0

Summary: A simple backup solution
Name: reoback
Version: 1.0.3
Release: %mkrel 8
License: GPL
URL: http://reoback.sourceforge.net/
Group: Archiving/Backup
BuildArchitectures: noarch
Requires: perl grep vixie-cron perl-libnet tar gzip
Source: http://prdownloads.sourceforge.net/reoback/%{name}-%{srcver}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
Pronounced as "Ray-o-back", REOBack is a simple backup solution designed
for Linux Users AND System Administrators. It is designed to be simple to
set-up and and easy to use. Great as a quick solution for those who
procrastinate about backups.

%prep
%setup -q -n %name-%tarver

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT/etc/reoback
mkdir -p $RPM_BUILD_ROOT/etc/cron.daily
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT/var/lib/reoback/{data,backups,tmp}

install reoback.pl $RPM_BUILD_ROOT%{_bindir}

install -m 644 docs/man/*.* $RPM_BUILD_ROOT%{_mandir}/man1

cat > $RPM_BUILD_ROOT/etc/reoback/files.conf << EOF
############################################################################
# REOBack Simple Backup Solution
# http://sourceforge.net/projects/reoback/
############################################################################
# Comments must start with a "#" as shown
############################################################################

# The following is an example with comments, below it is again without

# 'File:' followed by the name of the tar file that will be created
# Note that we don't include a path as that is added in the settings.conf
#File: TestFile1

# Simply list all directories to be recursively backed up (1 per line)
#/home/sforge

# 'Skip:' followed by any subdirectories you want not to be included
#	  from the above backup directory  
#Skip: /home/sforge/backups
#Skip: /home/sforge/reoback/data

# For files to be completely recursively backed up, don't use the 'Skip'
# option.  Simple, huh?
#/etc
#/home/frank

# Note we are starting a new backup file, but don't need to mark the close
# of the previous one
#File: TestFile2
#/var/www/html

# Note we can also include seperate files, not just directories
#/var/www/docs/hugedoc.txt
EOF
chmod 644 $RPM_BUILD_ROOT/etc/reoback/files.conf

install -m 600 conf/settings.conf $RPM_BUILD_ROOT/etc/reoback/

cat > $RPM_BUILD_ROOT/etc/cron.daily/reoback << EOF
#!/bin/sh

# check if all is configured
egrep -q '^[^#]*UNKNOWN' /etc/reoback/settings.conf

if [ \$? != 0 ]; then
  /usr/bin/reoback.pl /etc/reoback/settings.conf
fi

EOF
chmod 755 $RPM_BUILD_ROOT/etc/cron.daily/reoback

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc docs/{CHANGES,INSTALL,README,LICENSE}
%{_mandir}/man1/*
%dir /etc/reoback
%config(noreplace) /etc/reoback/*
/etc/cron.daily/reoback
/var/lib/reoback
%{_bindir}/*



%changelog
* Tue Sep 08 2009 Thierry Vignaud <tvignaud@mandriva.com> 1.0.3-8mdv2010.0
+ Revision: 433333
- rebuild

* Fri Aug 01 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.0.3-7mdv2009.0
+ Revision: 260212
- rebuild

* Fri Jul 25 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.0.3-6mdv2009.0
+ Revision: 248368
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tvignaud@mandriva.com> 1.0.3-4mdv2008.1
+ Revision: 126567
- kill re-definition of %%buildroot on Pixel's request
- use %%mkrel
- import reoback


* Mon Jan 10 2005 Frederic Lepied <flepied@mandrakesoft.com> 1.0.3-4mdk
- fix URL

* Sun Jan  9 2005 Frederic Lepied <flepied@mandrakesoft.com> 1.0.3-3mdk
- allow to have UNKNOWN in a comment

* Wed Aug  6 2003 Frederic Lepied <flepied@mandrakesoft.com> 1.0.3-2mdk
- rebuild

* Mon Mar 25 2002 Frederic Lepied <flepied@mandrakesoft.com> 1.0.3-1mdk
- removed patch0 integrated upstream
- 1.0.3

* Wed Aug 22 2001 Frederic Lepied <flepied@mandrakesoft.com> 1.0-1mdk
- first Mandrake Linux release
