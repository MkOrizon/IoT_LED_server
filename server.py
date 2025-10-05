from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

led_state = {"state": "OFF"}


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return """
    <html>
    <head>
        <title>ESP32 LED Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #0d1117;
                color: white;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }
            h1 {
                color: #58a6ff;
            }
            button {
                font-size: 1.2em;
                padding: 10px 20px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                margin-top: 20px;
                transition: 0.3s;
            }
            .on {
                background-color: #2ea043;
                color: white;
            }
            .off {
                background-color: #f85149;
                color: white;
            }
        </style>
    </head>
    <body>
        <h1>ESP32 LED Dashboard</h1>
        <h2 id="stateText">LED State: OFF</h2>
        <button id="toggleBtn" class="off" onclick="toggleLed()">Turn ON</button>

        <script>
            async function updateState() {
                const res = await fetch('/led/state');
                const data = await res.json();
                const stateText = document.getElementById('stateText');
                const btn = document.getElementById('toggleBtn');

                stateText.innerText = 'LED State: ' + data.state;
                if (data.state === 'ON') {
                    btn.innerText = 'Turn OFF';
                    btn.className = 'on';
                } else {
                    btn.innerText = 'Turn ON';
                    btn.className = 'off';
                }
            }

            async function toggleLed() {
                const res = await fetch('/led/state');
                const data = await res.json();
                const newState = data.state === 'ON' ? 'OFF' : 'ON';
                await fetch('/led/control/' + newState, { method: 'POST' });
                await updateState();
            }

            // Refresh LED state every 3 seconds
            setInterval(updateState, 3000);
            updateState();
        </script>
    </body>
    </html>
    """


@app.get("/led/state")
def get_led_state():
    print("[SERVER LOG] /led/state accessed → Current LED state:", led_state["state"])
    return led_state


@app.post("/led/control/{new_state}")
def control_led(new_state: str):
    global led_state
    if new_state.upper() in ["ON", "OFF"]:
        led_state["state"] = new_state.upper()
        print(f"[SERVER LOG] /led/control/{new_state} → LED turned {new_state.upper()} (Response Code: 200)")
        return JSONResponse(content={"message": f"LED turned {new_state.upper()}"}, status_code=200)
    else:
        print(f"[SERVER LOG] /led/control/{new_state} → Invalid command (Response Code: 400)")
        return JSONResponse(content={"error": "Invalid LED state"}, status_code=400)
