DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MoviePy MCP Dashboard</title>
    <style>
        :root {
            --primary-color: #3b82f6;
            --bg-color: #f3f4f6;
            --card-bg: #ffffff;
            --text-color: #1f2937;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
        }
        .card {
            background-color: var(--card-bg);
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        .card h2 {
            margin-top: 0;
            border-bottom: 1px solid #e5e7eb;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        button {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: 500;
            transition: background-color 0.2s;
        }
        button:hover {
            background-color: #2563eb;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
        }
        .action-btn {
            width: 100%;
            margin-bottom: 10px;
        }
        #status {
            margin-top: 10px;
            padding: 10px;
            border-radius: 4px;
            display: none;
        }
        .success { background-color: #d1fae5; color: #065f46; }
        .error { background-color: #fee2e2; color: #991b1b; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 MoviePy MCP Dashboard</h1>

        <div class="card">
            <h2>Clip Management</h2>
            <div class="grid">
                <button class="action-btn" onclick="callTool('list_clips')">📂 List Clips</button>
            </div>
            <div id="status"></div>
        </div>

        <div class="card">
            <h2>Quick Actions</h2>
            <div class="grid">
                <button class="action-btn" onclick="callTool('tools_check_installation')">🛠 Check Installation</button>
            </div>
        </div>

        <div class="card">
            <h2>Effects</h2>
            <p>Select a clip ID (copy from List Clips output) to apply effects.</p>
            <!-- In a real app, this would be more interactive -->
        </div>
    </div>

    <script>
        function sendAction(action) {
            if (window.parent) {
                console.log("Sending action to parent:", action);
                window.parent.postMessage(action, "*");
            } else {
                console.warn("No parent window found. Action:", action);
            }
        }

        function callTool(toolName, params = {}) {
            sendAction({
                type: "tool",
                payload: {
                    toolName: toolName,
                    params: params
                }
            });
            showStatus(`Requested execution of ${toolName}...`, 'success');
        }

        function showStatus(msg, type) {
            const el = document.getElementById('status');
            el.innerText = msg;
            el.className = type;
            el.style.display = 'block';
            setTimeout(() => {
                el.style.display = 'none';
            }, 3000);
        }
    </script>
</body>
</html>
"""
