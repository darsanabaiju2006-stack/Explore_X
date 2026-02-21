<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>


# ExploreX 🎯

## Basic Details

### Team Name: LUMINA

### Team Members
- Member 1: Sayoojya ks - SNM institute of management and technologies
- Member 2: Darsana Baiju - SNM institute of management and technologies

### Hosted Project Link
mention your project hosted link her

### Project Description
ExploreX: A Full-Stack Travel & Tourism Website. Built with Python and Flask, this project features a beautiful frontend for browsing travel packages and a powerful Admin Dashboard to manage bookings and users. It uses a SQL database to keep everything organized. Perfect for planning your next big adventure

### The Problem statement
Planning a trip is often messy because travel information is scattered everywhere. Small travel agencies struggle to show their packages and manage bookings manually using paper or basic spreadsheets, which leads to lost information and confused customers.

### The Solution
ExploreX solves this by providing a 'one-stop-shop' platform. It gives travelers a beautiful place to discover destinations and gives agency owners a simple digital dashboard to manage their entire business in one click.

---

## Technical Details

### Technologies/Components Used

**For Software:**
- Languages used: Python, HTML5, CSS3
- Frameworks used: Flask (Python Web Framework)
- Libraries used: Flask-SQLAlchemy (Database ORM), Jinja2 (Templating Engine), Werkzeug (Security utilities)
- Tools used: VS Code, Git, SQLite Browser



## Implementation

### For Software:

#### Installation
```bash
[# Clone the repository or extract the ZIP
# Navigate to the project folder
cd exploreX

# Install the required web framework
pip install flask flask-sqlalchemy]
```

#### Run
```bash
[# Initialize the database and seed initial data
python database.py

# Start the local development server
python app.py]
```



## Project Documentation

### For Software:

#### Screenshots (Add at least 3)

<img width="1917" height="800" alt="1" src="https://github.com/user-attachments/assets/913ecf72-4b64-4c02-88da-3c35ee8b1c6f" />


<img width="1905" height="887" alt="2" src="https://github.com/user-attachments/assets/d9e81216-ccb8-435c-83c8-236ff9ffd2b8" />


<img width="1884" height="900" alt="2 1" src="https://github.com/user-attachments/assets/95098eb5-9218-4df0-88ba-f87fa96fdfb0" />

<img width="1897" height="904" alt="3" src="https://github.com/user-attachments/assets/ed77eb2e-b2d9-47ee-9c9a-0566395191be" />


<img width="1837" height="868" alt="4" src="https://github.com/user-attachments/assets/af892d3a-af41-4bbc-9fd2-24a5d479835f" />


<img width="905" height="796" alt="5" src="https://github.com/user-attachments/assets/2b739a7c-6339-455a-bbcc-ffc9946b8d25" />


<img width="1902" height="912" alt="6" src="https://github.com/user-attachments/assets/844deb72-9179-45cc-a843-9d33f6a33e75" />

#### Diagrams

**System Architecture:**

The application follows a Request-Response cycle within a Client-Server Architecture.

Client Tier: The browser renders HTML/CSS and sends HTTP requests.

Server Tier: The Flask application processes logic, handles routing, and manages sessions.

Data Tier: SQLite serves as the persistent storage, managed via SQLAlchemy to ensure data integrity]
*Explain your system architecture - components, data flow, tech stack interaction*

<img width="975" height="879" alt="system archi" src="https://github.com/user-attachments/assets/7ff27614-88c6-4e03-8681-463985271d29" />


**Application Workflow:**

![Workflow](docs/workflow.png)
*Add caption explaining your workflow*

---


#### Build Photos

![Team](Add photo of your team here)

![Components](Add photo of your components here)
*List out all components shown*

![Build](Add photos of build process here)
*Explain the build steps*

![Final](Add photo of final product here)
*Explain the final build*

---

## Additional Documentation

### For Web Projects with Backend:

#### API Documentation

**Base URL:** `https://api.yourproject.com`

##### Endpoints

**GET /api/endpoint**
- **Description:** [What it does]
- **Parameters:**
  - `param1` (string): [Description]
  - `param2` (integer): [Description]
- **Response:**
```json
{
  "status": "success",
  "data": {}
}
```

**POST /api/endpoint**
- **Description:** [What it does]
- **Request Body:**
```json
{
  "field1": "value1",
  "field2": "value2"
}
```
- **Response:**
```json
{
  "status": "success",
  "message": "Operation completed"
}
```

[Add more endpoints as needed...]

---

### For Mobile Apps:

#### App Flow Diagram

![App Flow](docs/app-flow.png)
*Explain the user flow through your application*

#### Installation Guide

**For Android (APK):**
1. Download the APK from [Release Link]
2. Enable "Install from Unknown Sources" in your device settings:
   - Go to Settings > Security
   - Enable "Unknown Sources"
3. Open the downloaded APK file
4. Follow the installation prompts
5. Open the app and enjoy!

**For iOS (IPA) - TestFlight:**
1. Download TestFlight from the App Store
2. Open this TestFlight link: [Your TestFlight Link]
3. Click "Install" or "Accept"
4. Wait for the app to install
5. Open the app from your home screen

**Building from Source:**
```bash
# For Android
flutter build apk
# or
./gradlew assembleDebug

# For iOS
flutter build ios
# or
xcodebuild -workspace App.xcworkspace -scheme App -configuration Debug
```

---

### For Hardware Projects:

#### Bill of Materials (BOM)

| Component | Quantity | Specifications | Price | Link/Source |
|-----------|----------|----------------|-------|-------------|
| Arduino Uno | 1 | ATmega328P, 16MHz | ₹450 | [Link] |
| LED | 5 | Red, 5mm, 20mA | ₹5 each | [Link] |
| Resistor | 5 | 220Ω, 1/4W | ₹1 each | [Link] |
| Breadboard | 1 | 830 points | ₹100 | [Link] |
| Jumper Wires | 20 | Male-to-Male | ₹50 | [Link] |
| [Add more...] | | | | |

**Total Estimated Cost:** ₹[Amount]

#### Assembly Instructions

**Step 1: Prepare Components**
1. Gather all components listed in the BOM
2. Check component specifications
3. Prepare your workspace
![Step 1](images/assembly-step1.jpg)
*Caption: All components laid out*

**Step 2: Build the Power Supply**
1. Connect the power rails on the breadboard
2. Connect Arduino 5V to breadboard positive rail
3. Connect Arduino GND to breadboard negative rail
![Step 2](images/assembly-step2.jpg)
*Caption: Power connections completed*

**Step 3: Add Components**
1. Place LEDs on breadboard
2. Connect resistors in series with LEDs
3. Connect LED cathodes to GND
4. Connect LED anodes to Arduino digital pins (2-6)
![Step 3](images/assembly-step3.jpg)
*Caption: LED circuit assembled*

**Step 4: [Continue for all steps...]**

**Final Assembly:**
![Final Build](images/final-build.jpg)
*Caption: Completed project ready for testing*

---

### For Scripts/CLI Tools:

#### Command Reference

**Basic Usage:**
```bash
python script.py [options] [arguments]
```

**Available Commands:**
- `command1 [args]` - Description of what command1 does
- `command2 [args]` - Description of what command2 does
- `command3 [args]` - Description of what command3 does

**Options:**
- `-h, --help` - Show help message and exit
- `-v, --verbose` - Enable verbose output
- `-o, --output FILE` - Specify output file path
- `-c, --config FILE` - Specify configuration file
- `--version` - Show version information

**Examples:**

```bash
# Example 1: Basic usage
python script.py input.txt

# Example 2: With verbose output
python script.py -v input.txt

# Example 3: Specify output file
python script.py -o output.txt input.txt

# Example 4: Using configuration
python script.py -c config.json --verbose input.txt
```

#### Demo Output

**Example 1: Basic Processing**

**Input:**
```
This is a sample input file
with multiple lines of text
for demonstration purposes
```

**Command:**
```bash
python script.py sample.txt
```

**Output:**
```
Processing: sample.txt
Lines processed: 3
Characters counted: 86
Status: Success
Output saved to: output.txt
```

**Example 2: Advanced Usage**

**Input:**
```json
{
  "name": "test",
  "value": 123
}
```

**Command:**
```bash
python script.py -v --format json data.json
```

**Output:**
```
[VERBOSE] Loading configuration...
[VERBOSE] Parsing JSON input...
[VERBOSE] Processing data...
{
  "status": "success",
  "processed": true,
  "result": {
    "name": "test",
    "value": 123,
    "timestamp": "2024-02-07T10:30:00"
  }
}
[VERBOSE] Operation completed in 0.23s
```

---

## Project Demo

### Video
[Add your demo video link here - YouTube, Google Drive, etc.]

*Explain what the video demonstrates - key features, user flow, technical highlights*

### Additional Demos
[Add any extra demo materials/links - Live site, APK download, online demo, etc.]

---

## AI Tools Used (Optional - For Transparency Bonus)

If you used AI tools during development, document them here for transparency:

**Tool Used:** [e.g., GitHub Copilot, v0.dev, Cursor, ChatGPT, Claude]

**Purpose:** [What you used it for]
- Example: "Generated boilerplate React components"
- Example: "Debugging assistance for async functions"
- Example: "Code review and optimization suggestions"

**Key Prompts Used:**
- "Create a REST API endpoint for user authentication"
- "Debug this async function that's causing race conditions"
- "Optimize this database query for better performance"

**Percentage of AI-generated code:** [Approximately X%]

**Human Contributions:**
- Architecture design and planning
- Custom business logic implementation
- Integration and testing
- UI/UX design decisions

*Note: Proper documentation of AI usage demonstrates transparency and earns bonus points in evaluation!*

---

## Team Contributions

- [Name 1]: [Specific contributions - e.g., Frontend development, API integration, etc.]
- [Name 2]: [Specific contributions - e.g., Backend development, Database design, etc.]
- [Name 3]: [Specific contributions - e.g., UI/UX design, Testing, Documentation, etc.]

---

## License

This project is licensed under the [LICENSE_NAME] License - see the [LICENSE](LICENSE) file for details.

**Common License Options:**
- MIT License (Permissive, widely used)
- Apache 2.0 (Permissive with patent grant)
- GPL v3 (Copyleft, requires derivative works to be open source)

---

Made with ❤️ at TinkerHub
