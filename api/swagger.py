from flask import jsonify

def swagger_spec():
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "Dolev Atik & Yahav Vituri , AI RAG Agent API  ",
            "version": "1.0.0",
            "description": "API for an AI agent capable of answering questions based on academic research papers using RAG."
        },
        "servers": [
            {"url": "http://localhost:5000/api"}
        ],
        "paths": {
            "/papers": {
                "post": {
                    "summary": "Upload PDF research papers",
                    "requestBody": {
                        "content": {
                            "multipart/form-data": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "files": {
                                            "type": "array",
                                            "items": {
                                                "type": "string",
                                                "format": "binary"
                                            }
                                        }
                                    },
                                    "required": ["files"]
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "Papers uploaded successfully"}
                    }
                }
            },
            "/query": {
                "post": {
                    "summary": "Query the RAG agent",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/QueryRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AnswerResponse"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "QueryRequest": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string", "example": "What are the effects of climate change on agriculture?"}
                    },
                    "required": ["question"]
                },
                "SourceCitation": {
                    "type": "object",
                    "properties": {
                        "document_name": {"type": "string", "example": "research_paper_1.pdf"},
                        "chunk_id": {"type": "string", "example": "chunk_0"}
                    }
                },
                "AnswerResponse": {
                    "type": "object",
                    "properties": {
                        "answer": {"type": "string", "example": "Climate change leads to more frequent droughts and changes in precipitation patterns, negatively impacting agricultural yields."},
                        "citations": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/SourceCitation"}
                        },
                        "confidence_score": {"type": ["number", "null"], "format": "float", "example": 0.85}
                    }
                }
            }
        }
    })