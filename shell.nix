with (import <nixpkgs>{});

stdenv.mkDerivation {
  name = "shell";
  buildInputs = [
    python37Full
    python37Packages.google_api_python_client
    python37Packages.google-auth-httplib2
    python37Packages.google-auth-oauthlib
    python37Packages.notify2
    python37Packages.scipy
  ];
}
