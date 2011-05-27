#version 120
#extension all : disable

#if (__VERSION__ > 120)
in vec4 gl_Vertex;
#endif

uniform vec3 translation;
uniform mat4 transformation;

void main ()
{
  gl_Position = transformation * (vec4(translation, 0.0) + gl_Vertex);
} 
