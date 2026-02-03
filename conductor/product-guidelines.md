# Product Guidelines

## Tone and Style
- **Technical & Precise:** Tool descriptions and responses must be technical and precise. Focus on exact parameters, types, and the direct mapping to MoviePy methods. This ensures clarity for both developers and AI agents interacting with the server.

## Documentation and Mapping
- **Strict Documentation Mapping:** Every MCP tool and internal helper function must include a docstring that explicitly references the corresponding documentation file or section within the local `html/` directory. This ensures that the local MoviePy documentation remains the single source of truth for implementation logic and API behavior.

## Implementation Standards
- **MoviePy Alignment:** All code should strictly follow the architectural patterns and API specifications defined in the provided MoviePy documentation.
- **Error Handling:** Errors returned by the MCP server should be descriptive, mapping MoviePy exceptions to clear, actionable messages for the end-user or agent.
