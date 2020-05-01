with (import <nixpkgs>{});

stdenv.mkDerivation {
  name = "shell";
  buildInputs = [
    R
    rPackages.ggplot2
    rPackages.knitr
    rPackages.codetools
    rPackages.rmarkdown
    rPackages.lubridate
    rPackages.dplyr
    pandoc
    haskellPackages.pandoc-citeproc
    # haskellPackages.pandoc-crossref
  ];
}
