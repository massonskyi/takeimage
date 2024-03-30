class ErrorCodes:
    API_LOAD_SUCCESS = 1000
    API_LOAD_FAILED = -1000

    MODELS_LOAD_SUCCESS = 2000
    MODELS_LOAD_REQUEST_FAILED = -2001
    MODELS_LOAD_KEY_ERROR = -2002
    MODELS_LOAD_JSON_DECODE_ERROR = -2003
    MODELS_LOAD_UNKNOWN_ERROR = -2004

    IMAGE_GENERATION_STARTED = 3000
    IMAGE_GENERATION_REQUEST_FAILED = -3001
    IMAGE_GENERATION_JSON_DECODE_ERROR = -3002
    IMAGE_GENERATION_KEY_ERROR = -3003
    IMAGE_GENERATION_UNKNOWN_ERROR = -3004

    GENERATION_COMPLETED = 4000
    GENERATION_TIMEOUT = -4001
    GENERATION_REQUEST_FAILED = -4002
    GENERATION_JSON_DECODE_ERROR = -4003
    GENERATION_UNKNOWN_ERROR = -4004
    GENERATION_STATUS_NOT_FOUND = -4005

    ERROR_CODES_PROTOCOL = {
        API_LOAD_SUCCESS: "Text2ImageAPI successfully loaded",
        API_LOAD_FAILED: "KANDINSKY_TOKEN or KANDINSKY_SECRET_KEY not setup",

        MODELS_LOAD_SUCCESS: "Models successfully loaded",
        MODELS_LOAD_REQUEST_FAILED: "Failed to load models due to a request exception",
        MODELS_LOAD_KEY_ERROR: "Failed to load models due to a key error",
        MODELS_LOAD_JSON_DECODE_ERROR: "Failed to load models due to a JSON decode error",
        MODELS_LOAD_UNKNOWN_ERROR: "Failed to load models due to an unknown error",

        IMAGE_GENERATION_STARTED: "Starting image generation",
        IMAGE_GENERATION_REQUEST_FAILED: "Failed to generate image due to a request exception",
        IMAGE_GENERATION_JSON_DECODE_ERROR: "Failed to generate image due to a JSON decode error",
        IMAGE_GENERATION_KEY_ERROR: "Failed to generate image due to a key error",
        IMAGE_GENERATION_UNKNOWN_ERROR: "Failed to generate image due to an unknown error",

        GENERATION_COMPLETED: "Generation completed",
        GENERATION_TIMEOUT: "Generation request timed out",
        GENERATION_REQUEST_FAILED: "Failed to check generation status due to a request exception",
        GENERATION_JSON_DECODE_ERROR: "Failed to check generation status due to a JSON decode error",
        GENERATION_UNKNOWN_ERROR: "Failed to check generation status due to an unknown error",
        GENERATION_STATUS_NOT_FOUND: "Generation status not found in response data",
    }