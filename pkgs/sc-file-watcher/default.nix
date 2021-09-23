with import <nixpkgs> {};

pkgs.python39Packages.buildPythonApplication {
  pname = "sc-file-watcher";
  src = ./.;
  version = "0.1";
  buildInputs = [
   pkgs.python39Packages.setuptools
   pkgs.python39Packages.pip
   pkgs.python39];
  propagatedBuildInputs = [ pkgs.python39Packages.pip
   pkgs.python39Packages.azure-storage-blob
   pkgs.python39Packages.prometheus_client
   pkgs.python39Packages.timeout-decorator
   pkgs.python39Packages.setuptools
   pkgs.python39
   
];

}
