import os
import sys
import licant.make
import glob

error_in_install_library = False
termux_dir = "/data/data/com.termux/files/home"

is_termux = "ANDROID_ROOT" in os.environ
is_windows = sys.platform == 'win32'

def find_application_path():
	global error_in_install_library

	path_list = os.environ["PATH"].split(":")
	
	if "/usr/local/bin" in path_list:
		path = "/usr/local/bin"
	
	else:
		print("DebugMode")
		for p in path_list:
			print(p)
			print("/usr/bin" in p)
			if "/usr/bin" in p:
				path = p
				print(f"path found: {path}")
				break 
		else:
			print("Warning: Install path not found")
			error_in_install_library = True

	return path

def find_headers_path():
	global error_in_install_library

	if is_termux:
		return os.path.join(termux_dir, "usr/include")
	
	if is_windows:
		print("TODO: Windows support")
		error_in_install_library = True
		return None
	
	return "/usr/local/include"

def find_libraries_path():
	global error_in_install_library

	if is_termux:
		return os.path.join(termux_dir, "usr/lib")

	if is_windows:
		print("TODO: Windows support")
		error_in_install_library = True
		return None
	
	return "/usr/lib"


path = find_application_path()
headers_path = find_headers_path()
libraries_path = find_libraries_path()
		
def install_application(src, newname=None):
	if error_in_install_library:
		return None

	if newname is None:
		newname = os.path.basename(src)

	tgt = os.path.join(path, newname)
	licant.make.copy(tgt=tgt, src=src)

	return tgt

def install_headers(tgtdir, srcdir, patterns=("*.h", "*.hxx")):
	lsts = [ glob.glob(os.path.join(os.path.abspath(srcdir), p)) for p in patterns ]
	
	headers = []
	for lst in lsts:
		headers.extend(lst)

	for h in headers:
		licant.source(h)

	targets = [ licant.copy(src=h, tgt=os.path.join(headers_path, tgtdir, os.path.relpath(h, srcdir))) for h in headers ]
	full_target = licant.fileset(tgt="headers://"+srcdir, targets=targets)	

	return full_target

def install_shared_library(src, newname=None):
	if error_in_install_library:
		return None

	if newname is None:
		newname = os.path.basename(src)

	tgt = os.path.join(libraries_path, newname)
	licant.make.copy(tgt=tgt, src=src)

	return tgt

def install_library(tgt, libtgt, hroot, headers, headers_patterns=("*.h", "*.hxx")):
	if error_in_install_library:
		return None

	ltgt = install_shared_library(libtgt)
	htgt = install_headers(tgtdir=hroot, srcdir=headers, patterns=headers_patterns)

	tgts = [ htgt, ltgt ]

	return licant.fileset(tgt=tgt, targets=tgts)
