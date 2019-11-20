from picoweb import WebApp, start_response, jsonify
from machine import Pin
import uasyncio as asyncio
import gc

pin2 = Pin(2, Pin.OUT)
pin2.on()

app = WebApp(__name__)


async def toggle(pin):
  if pin.value() == 0:
    pin.value(1)
    return True
  else:
    pin.value(0)
    return False


@app.route("/free_mem/")
async def free_mem(req, resp):
  return await jsonify(
    resp,
    {
      "free_mem": gc.mem_free()
    }
  )


async def coro_gc_collect():
  while True:
    # print("Freeing memory.")
    gc.collect()
    await asyncio.sleep(20)


@app.route("/")
async def index(req, resp):
  await start_response(resp)
  return await resp.awrite("""
  <html>
  
  <head>
    <script src="/static/js/jquery.min.js"></script>
  </head>
  
  <style>
  .toggle_button {{
    height:200px;
    width:200px;
    font-size:20px;
  }}
  </style>
  
  <body>
    <center>
      <h1>Hello from the ESP8266 running a web server!</h1>
      <p>
        <h1>Current free memory:
          <span id="mem_free" name="mem_free"></span> bytes
        </h1>
      </p>
      <p>
        <input class="toggle_button" type="button" id="toggle_2" name="toggle_2" value="Toggle LED" onclick="toggleLED2();"/>
      </p>
    </center>
  </body>
  
  <script type='text/javascript'>

  function loadFreeMem() {{
    $.getJSON("free_mem/", function(data) {{
      var free = data['free_mem'];
      $('#mem_free').html(free);
    }});
  }}

  function toggleLED2() {{
    $.getJSON("/toggle_2/", function(data) {{console.log(data)}});
  }}

  $(document).ready( function() {{
    
    // alert("ready.");
    
    loadFreeMem();

    window.setInterval(
      function() {{
        loadFreeMem();
      }},
      2500
    );

  }});
  </script>
  </html>
  """.format(gc.mem_free())
  )


@app.route("/t/")
async def t(req, resp):
  return await resp.awrite("t")
  

@app.route("/json/")
async def json(req, resp):
  return await jsonify(
    resp,
    {
      "ID": 1,
      "Name": "Jared",
    }
  )


@app.route("/toggle_2/")
async def toggle_2(req, resp):
  status = await toggle(pin2)
  return await jsonify(
    resp,
    {
      "state": status
    }
  )


def serve():
  loop = asyncio.get_event_loop()            # event loop
  loop.create_task(coro_gc_collect())        # coroutine - garbage collection 
  app.run(debug=1, host="0.0.0.0", port=80)  # Start server
  
  
if __name__ == "__main__":
  serve()

