# Ultimatum (under HEAVY development)

Ultimatum is a *new* kind of Wayland compositor.   
Not just a cool, innovative, "new paradigm" of tiling window manager, UM is an entirely different philosophy altogether.   
   
---

## User-facing

Every "desktop environment" is rendered and described via a bundled, HTML/CSS/JS website (some may call it a "Web OS"), which handles, renders and composites windows.   
Each of these websites (desktop environments) may:
- Internally describe widgets and extensions
    - Widgets: Separate, modular "iframe" websites for a specific purpose
        - Can register settings
    - Extensions: Regular JS files that have access to the framework-agnostic API
        - Can communicate with the registered DE
        - Can receive live window image data and render it to a canvas via the API
        - Can register settings
- Describe styles and scripts separate from the API
    - E.G. the scripts would be your React bundle
- Register global keybinds to:
    - Trigger some event on the local page
    - Forward a message to an extension
OR:
- Specify an external dependency (extension, widget, etc) and load it in
   
Widgets and extensions may also be manually registered by the user regardless of potential conflicts.

## Internals

- WPE webkit will be used (don't worry, when Servo is stable we'll consider it!) to render desktop environments and receive/send WebSocket events.
- Backend will internally process damage buffers and rendered window data, copy by DMABUF and (JS API) renders to an OpenGL canvas in the compositor.
- Communication by IPC - Register global keybinds, manipulate windows, receive/edit window properties.
    - JS API communicates, receives, renders window props and events to/from the frontend (THIS renderer), passed to the backend
- 

## Pros/Cons
| Pro | Con |
|-----|-----|
| Easy to develop WM/DE if you have little-to-know Wayland know-how. | All tiling, floating, layout paradigms, must be implemented yourself\*. |
| Decently simple IPC. | Primarily, commands/shell scripts supported (yay!). Advanced features require exposed and abstracted `dyncall`. |
| Can load entire DE from a server-side application. | No routing possible\*\* |

\* *Layout library may be possible*   
\*\* *Unless you use React (or another router that primarily replaces the root element)*

**WE ARE STILL DRAFTING THE PROCESS FOR RENDERING AND HANDLING LIKE 40% OF THIS. BE PATIENT**