<h1>Stella Bot</h1>

<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/speech_recognition-4B8BBE?style=flat-square&logo=google&logoColor=white" alt="speech_recognition">
  <img src="https://img.shields.io/badge/pyttsx3-3776AB?style=flat-square&logo=python&logoColor=white" alt="pyttsx3">
  <img src="https://img.shields.io/badge/Wikipedia-000000?style=flat-square&logo=wikipedia&logoColor=white" alt="Wikipedia">
</p>

<blockquote><em>A small voice assistant in Python — talk, it answers out loud. Opens sites, pulls Wikipedia summaries, tells jokes, reads the time.</em></blockquote>

<hr>

<h2>The question</h2>

<p>A small voice assistant in Python. You talk, it answers out loud, and it can open a few sites, pull two sentences from Wikipedia, tell a joke, or read the time.</p>

<p>This is a rule-based script, not an LLM. It looks for keywords in what Google Speech-to-Text heard.</p>

<p>The code is <a href="Stella.py"><code>Stella.py</code></a>.</p>

<hr>

<h2>What it does</h2>

<table>
  <thead>
    <tr>
      <th>You say something like</th>
      <th>It does</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>"what can you do"</td>
      <td>lists the skills below</td>
    </tr>
    <tr>
      <td>"open youtube / google / github / facebook / instagram / stackoverflow / amazon / flipkart / ebay"</td>
      <td>opens that site in the browser</td>
    </tr>
    <tr>
      <td>"wikipedia &lt;topic&gt;"</td>
      <td>reads a 2-sentence Wikipedia summary</td>
    </tr>
    <tr>
      <td>"the time"</td>
      <td>speaks the current clock time</td>
    </tr>
    <tr>
      <td>"open code"</td>
      <td>starts VS Code if the path in <code>Stella.py</code> exists</td>
    </tr>
    <tr>
      <td>"tell me a joke" / "say a joke"</td>
      <td>picks one from a hardcoded list</td>
    </tr>
    <tr>
      <td>"exit"</td>
      <td>says goodbye and stops</td>
    </tr>
  </tbody>
</table>

<p>Speech in: <code>speech_recognition</code> + the default microphone + Google's recognizer (<code>en-in</code>). Speech out: <code>pyttsx3</code> (SAPI5 on Windows, default driver elsewhere).</p>

<hr>

<h2>Tech stack</h2>

<table>
  <thead>
    <tr><th>Layer</th><th>Tools</th></tr>
  </thead>
  <tbody>
    <tr><td>Language</td><td>Python 3</td></tr>
    <tr><td>Speech in</td><td><code>speech_recognition</code> + Google Web Speech API (<code>en-in</code>)</td></tr>
    <tr><td>Speech out</td><td><code>pyttsx3</code> (SAPI5 on Windows, default driver elsewhere)</td></tr>
    <tr><td>Web lookup</td><td><code>wikipedia</code> Python package (2-sentence summaries)</td></tr>
    <tr><td>Browser control</td><td><code>webbrowser</code> stdlib module</td></tr>
    <tr><td>Architecture</td><td>Rule-based keyword matching (not an LLM)</td></tr>
  </tbody>
</table>

<hr>

<h2>How to run</h2>

<p>Needs a microphone and, for recognition, an internet connection.</p>

<pre><code>python -m pip install -r requirements.txt
python Stella.py</code></pre>

<p>On Windows, install PyAudio from a wheel if <code>pip install pyaudio</code> fails. On Linux you usually need PortAudio first (<code>portaudio19-dev</code>).</p>

<p>If VS Code is not at <code>D:\Installs\Microsoft VS Code\Code.exe</code>, change <code>VSCODE_PATH</code> at the top of <code>Stella.py</code>.</p>

<hr>

<h2>Layout</h2>

<pre><code>Stella.py           the assistant
README.md           this file
requirements.txt</code></pre>

<table>
  <thead>
    <tr><th>File you started with</th><th>Where it lives now</th></tr>
  </thead>
  <tbody>
    <tr><td><code>Stella.py</code></td><td><code>Stella.py</code></td></tr>
    <tr><td><code>README.md</code></td><td>this file</td></tr>
    <tr><td><code>requirements.txt</code></td><td><code>requirements.txt</code></td></tr>
  </tbody>
</table>

<hr>

<h2>Limits</h2>

<ul>
  <li>It only reacts to the phrases in the table. Anything else is ignored.</li>
  <li>Recognition goes through Google. Offline speech is not set up.</li>
  <li>Wikipedia and the browser commands need the network.</li>
  <li>"Open code" is a single hardcoded path, not a search of the Start Menu.</li>
  <li>Jokes are a fixed list in the file. <code>pyjokes</code> is listed in some older notes; this script does not call it.</li>
</ul>

<hr>

<h2>License</h2>

<p>Use it as you like. Wikipedia text belongs to Wikipedia.</p>
