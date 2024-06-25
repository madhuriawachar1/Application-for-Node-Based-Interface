
![alt text](<workingappss.png>)
![alt text](<withbackend_response.png>)

# Part 1: Node Abstraction

By using the Node component as a base, we can significantly reduce the code for each specific node type. Instead of duplicating logic for rendering labels, inputs, and handles, we delegate these responsibilities to the Node component. Specific nodes only need to define their unique inputs and any additional custom logic.


State Management, Event Handlers, Rendering Logic, etc are all handled by the Node component. This allows us to focus on the unique logic for each node type.


# Part 2: Styling

see ` frontend/src/index.css ` for styling.


use: tailwind


#  Part 3: Text Node Logic

## Task 1: Dynamically Adjusting the Textarea Size

Dynamically Adjusting the Textarea Size
The first task is to dynamically adjust the size of the textarea based on the content.

1. State Initialization:

currText: Holds the current text input value.
inputHeight: Manages the height of the textarea, initially set to 20 pixels.

2. Refs:

spanRef: A reference to a hidden span element used to calculate text width.
inputRef: A reference to the textarea element.

3. Text Change Handler:This function updates the state whenever the text input changes.

4. Effect Hook to Adjust Textarea Size:

```
useEffect(() => {
  const span = spanRef.current;
  const input = inputRef.current;
  if (span && input) {
    span.innerText = currText || '{{input}}';
    const width = span.offsetWidth;
    const maxWidth = 500; // Set your max width here

    if (width + 10 <= maxWidth) {
      input.style.width = `${width + 10}px`; // Add some padding to avoid cutting off text
      input.style.height = 'auto'; // Reset height
      setInputHeight(20); // Reset to default height if width is under max
    } else {
      input.style.width = `${maxWidth}px`;
      const lines = Math.ceil((width + 10) / maxWidth); // Calculate number of lines
      setInputHeight(20 + lines * 20); // Increase height based on number of lines
    }
  }
}, [currText]);

```

1. The effect runs whenever currText changes.
2. The hidden span's inner text is set to currText.
3. The span's width is used to adjust the textarea's width.
4. If the text width exceeds maxWidth, the height of the textarea is adjusted based on the number of lines.


## Task 2: Adding a Handle

1. State Initialization:

handles: Holds an array of handle objects, each representing a detected variable.

2. Effect Hook to Detect Variables:

```
useEffect(() => {
  const variableRegex = /\{\{(.*?)\}\}/g;
  const matches = [];
  let match;

  while ((match = variableRegex.exec(currText)) !== null) {
    matches.push(match[1].trim());
  }

  const newHandles = matches.map((variable, index) => ({
    id: `${id}-input-${index}`,
    variable,
  }));

  setHandles(newHandles);
}, [currText, id]);

```

* The effect runs whenever currText or id changes.

* It uses a regular expression to find variables enclosed in double curly brackets ({{variable}}).

* For each detected variable, it creates a handle object and updates the handles state.


3. Rendering Handles:
```
{handles.map((handle, index) => (
  <Handle
    key={handle.id}
    type="target"
    position={Position.Left}
    id={handle.id}
    style={{ top: `${20 + index * 20}px` }} // Adjust the position of each handle
  />
))}

```
* This maps over the handles array and renders a Handle component for each detected variable.

### Example:
Hello, {{name}}! Your order {{orderId}} is ready for pickup.

* The regex /\{\{(.*?)\}\}/g matches any text enclosed in double curly brackets.
* It finds two matches: {{name}} and {{orderId}}.
* These matches are trimmed and stored in the matches array: ["name", "orderId"].



# Part 4: Backend Integration

## Task 1: Sending Pipeline Data to the Backend (in submit.js)

1. Transform the Nodes: The nodes from the state are transformed into the desired format, with position and data fields containing additional properties.
2. Transform the Edges: The edges from the state are transformed into the desired format.
3. Create the Payload: The formatted nodes and edges are combined into a payload object.
4. Send the Payload: The payload is sent to the backend using an HTTP POST request via axios.

## In ` backend/main.py `.
1. CORS configuration
```
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```


1. Explanation of the Endpoint
Route Definition:

@app.post("/pipelines/parse"): This decorator defines a POST endpoint at /pipelines/parse.

2. Data Models:

Node: Represents a node in the pipeline with an id, type, position, and data.
Edge: Represents an edge in the pipeline with an id, source, and target.

Pipeline: Represents the entire pipeline consisting of a list of Node and Edge.

3. Endpoint Function:

def parse_pipeline(pipeline: Pipeline): This function receives the pipeline data as input.

4. Processing:

Calculates the number of nodes and edges.
Constructs a graph representation from the nodes and edges.
Checks if the graph is a Directed Acyclic Graph (DAG) using Depth-First Search (DFS).


5. Response:

Returns a JSON response with the number of nodes, edges, and whether the graph is a DAG.

# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
