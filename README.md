# ckdupes

Inspiration: https://github.com/platypusguy/FileDedupe

All duplicate files are reported while walking the directory tree on the command line.  Nothing is altered.

Definition of a duplicate: the file byte size and checksum match an existing entry.  The file path is irrelevant to matching.

Sample invocation:

     python3   ckdupes_main.py   {Directory to be traversed}

Simple invocation i.e. without option specifications:

```
python3   ckdupes_main.py   /var/lib/apt


Begin
*** Skipping file /var/lib/apt/lists/lock, permission denied
*** Skipping directory /var/lib/apt/lists/partial, permission denied
/var/lib/apt/lists/mirror.lstn.net_ubuntu_dists_focal-updates_restricted_binary-i386_Packages	-is a duplicate of-
	/var/lib/apt/lists/mirror.lstn.net_ubuntu_dists_focal-security_restricted_binary-i386_Packages
/var/lib/apt/lists/repo.vivaldi.com_stable_deb_dists_stable_main_Contents-i386.lz4	-is a duplicate of-
	/var/lib/apt/lists/repo.vivaldi.com_stable_deb_dists_stable_main_Contents-amd64.lz4
*** Skipping file /var/lib/apt/daily_lock, nil content
*** Skipping file /var/lib/apt/periodic/upgrade-stamp, nil content
*** Skipping file /var/lib/apt/periodic/update-success-stamp, nil content
*** Skipping file /var/lib/apt/periodic/download-upgradeable-stamp, nil content
*** Skipping file /var/lib/apt/periodic/unattended-upgrades-stamp, nil content
*** Skipping file /var/lib/apt/periodic/update-stamp, nil content
Elapsed seconds = 0.87
Scanned a total of 6 subdirectories and 106 files
File duplicates: 2
Directory permission issues: 1
File permission issues: 1
Files with nil content: 6
End
```

Omitting the logging of skipped files and directories:

```
python3   ckdupes_main.py   /var/lib/apt   -s

Begin
/var/lib/apt/lists/mirror.lstn.net_ubuntu_dists_focal-updates_restricted_binary-i386_Packages	-is a duplicate of-
	/var/lib/apt/lists/mirror.lstn.net_ubuntu_dists_focal-security_restricted_binary-i386_Packages
/var/lib/apt/lists/repo.vivaldi.com_stable_deb_dists_stable_main_Contents-i386.lz4	-is a duplicate of-
	/var/lib/apt/lists/repo.vivaldi.com_stable_deb_dists_stable_main_Contents-amd64.lz4
Elapsed seconds = 0.91
Scanned a total of 6 subdirectories and 106 files
File duplicates: 2
Directory permission issues: 1
File permission issues: 1
Files with nil content: 6
End
```


Processing only at the top directory level:

```
python3   ckdupes_main.py   /var/lib/apt   -n

Begin
*** Skipping file /var/lib/apt/daily_lock, nil content
Scanned a total of 0 subdirectories and 3 files
No duplicates detected
Directory permission issues: 0
File permission issues: 0
Files with nil content: 1
End
```

Feel free to open an issue, especially if you find any bugs. I'll respond as soon as I can.

Richard Elkins

Dallas, Texas, USA, 3rd Rock, Sol, ...

