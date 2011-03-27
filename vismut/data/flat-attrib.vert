#version 120
#extension all : disable

attribute vec4 the_color;

uniform vec3 translation;
uniform mat4 transformation;

varying vec4 color;

#if (__VERSION__ > 120)
in vec4 gl_Vertex;
#endif

void main ()
{
  gl_Position = transformation * (vec4(translation, 0.0) + gl_Vertex);

  color = the_color;
} 
