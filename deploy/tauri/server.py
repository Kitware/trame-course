from trame.app import demo

if __name__ == "__main__":
    cone = demo.Cone()

    @cone.ctrl.add("on_server_ready")
    def port_used(**kwargs):
        print(f"tauri-server-port={cone.server.port}", flush=True)

    # Default args when run as app: port=0, open_browser=False, timeout=10
    cone.server.start()
