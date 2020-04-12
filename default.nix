with (import <nixpkgs>{});

python37Packages.buildPythonPackage rec {
  name = "ctrl-email-${version}";
  version = "1.0";

  src = fetchTarball("https://github.com/GuilloteauQ/Ctrl-Email/tarball/master");
  propagatedBuildInputs = with python37Packages; [
    google_api_python_client
    google-auth-httplib2
    google-auth-oauthlib
    notify2
  ];

  doCheck = false;

  postInstall = ''
    cp -r app/ $out
  '';
}
