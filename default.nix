{ system ? builtins.currentSystem }:                                                   
                                                                                   
let                                                                                    
   pkgs = import <nixpkgs> { inherit system; };                                         
                                                                                   
   callPackage = pkgs.lib.callPackageWith (pkgs // self);                               
                                                                                   
   self = {                                                                             
      sc-file-watcher = callPackage ./pkgs/sc-file-watcher { };    
      lammps =  callPackage ./pkgs/lammps { };

   };                                                                                   
in self 
