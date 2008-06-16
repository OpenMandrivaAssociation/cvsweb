Summary:	Visual (www) interface to explore a cvs repository
Name:		cvsweb
Version:	3.0.6
Release:	%mkrel 5
Epoch:		1
License:	BSD
Group:		System/Servers
URL:		http://www.FreeBSD.org/projects/cvsweb.html
Source0:	http://people.freebsd.org/~scop/cvsweb/%{name}-%{version}.tar.bz2
Patch:		cvsweb-3.0.5.config.patch
Requires:	cvs
Requires:	rcs
Requires:	apache >= 2.0.54
Requires(post):   rpm-helper >= 0.16
Requires(postun): rpm-helper >= 0.16
BuildRequires:    rpm-helper >= 0.16
BuildRequires:	ImageMagick
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
cvsweb is a visual (www) interface to explore a cvs repository. This is an
enhanced cvsweb developed by Henner Zeller. Enhancements include recognition
and display of popular mime-types, visual, color-coded, side by side diffs
of changes and the ability sort the file display and to hide old files
from view. One living example of the enhanced cvsweb is the KDE cvsweb

cvsweb requires the server to have cvs and a cvs repository worth exploring.

%prep

%setup -q
%patch -p 1 -b .config
for file in icons/*.gif; do
    convert $file icons/`basename $file gif`png
    rm -f $file
done

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_var}/www/cgi-bin
install -d -m 755 %{buildroot}%{_var}/www/%{name}
install -d -m 755 %{buildroot}%{_sysconfdir}
install -d -m 755 %{buildroot}%{_datadir}/enscript/hl
install -m 755 cvsweb.cgi %{buildroot}%{_var}/www/cgi-bin
install -m 644 cvsweb.conf %{buildroot}%{_sysconfdir}
install -m 644 css/* %{buildroot}%{_var}/www/%{name}
install -m 644 icons/* %{buildroot}%{_var}/www/%{name}
install -m 644 enscript/* %{buildroot}%{_datadir}/enscript/hl

# apache configuration
install -d -m 755 %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf <<EOF
# cvsweb configuration

<IfModule mod_perl.c>
    PerlSwitches -T
</IfModule>

Alias /cvsweb /var/www/cvsweb

<Directory /var/www/cvsweb>
    Order Deny,Allow
    Deny from All
    Allow from All
</Directory>

<Location /cgi-bin/cvsweb.cgi>
    <IfModule mod_perl.c>
	SetHandler perl-script
	PerlResponseHandler ModPerl::Registry
	PerlOptions +ParseHeaders
    </IfModule>
    Order Deny,Allow
    Deny from All
    Allow from All
</Location>

EOF

cat > README.mdv <<EOF

Mandriva RPM specific notes

setup
-----
The setup used here differs from default one, to achieve better FHS compliance.
- the files accessibles from the web are in /var/www/cvsweb
- the configuration file is /etc/cvsweb.conf

Suggested packages
------------------
- enscript for syntax highlighting
- cvsgraph for cvs graphs
- cvshistory for cvs history

EOF

%post
%_post_webapp

%postun
%_postun_webapp

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog INSTALL NEWS README TODO README.mdv cvsweb.conf-*
%config(noreplace) %{_sysconfdir}/cvsweb.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%{_var}/www/cgi-bin/cvsweb.cgi
%{_var}/www/%{name}
%{_datadir}/enscript/hl/*


