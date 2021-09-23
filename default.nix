{ system ? builtins.currentSystem }:                                                   
                                                                                   
let                                                                                    
   pkgs = import <nixpkgs> { inherit system; };                                         
                                                                                   
   callPackage = pkgs.lib.callPackageWith (pkgs // self);                               
                                                                                   
   self = {                                                                             
      lammps = callPackage ./pkgs/lammps { };    
      hello-test = callPackage ./pkgs/hello-test { }; 
      test = callPackage ./pkgs/test { }; 
   };                                                                                   
in self 
