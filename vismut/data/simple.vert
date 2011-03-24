#version 120
#extension all : disable

uniform vec3 translation;
uniform mat4 transformation;

#if (__VERSION__ > 120)
in vec4 gl_Vertex;
#endif

void main ()
{
  gl_Position = transformation * (vec4(translation, 0.0) + gl_Vertex);
} 
