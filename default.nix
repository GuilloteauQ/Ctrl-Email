with (import <nixpkgs>{});

let
  app_name = "ctrl-email";
  app_version = "1.0";
in {
  ctrl_email = python37Packages.buildPythonPackage rec {
    name = "${app_name}-${version}";
    version = "${app_version}";

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
  };

  # systemd.user.services.ctrl-email = {
  #   wantedBy = [ "multi-user.target" ];
  #   serviceConfig = {
  #     ExecStart = "${pkgs.ctrl_email}/ctrl_email";
  #     KillMode = "process";
  #     Restart = "always";
  #     Type = "simple";
  #   };
  # };

  # systemd.services.ctrl-email.enable = true;
}
