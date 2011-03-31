#version 120
#extension all : disable

#if (__VERSION__ > 120)
in vec4 gl_Vertex;
#endif

#if (__VERSION__ <= 120)
attribute vec4 color;
#else
in vec4 color;
#endif

uniform vec3 translation;
uniform mat4 transformation;

#if (__VERSION__ <= 120)
varying vec4 the_color;
#else
out vec4 the_color;
#endif

void main ()
{
  gl_Position = transformation * (vec4(translation, 0.0) + gl_Vertex);

  the_color = color;
} 
