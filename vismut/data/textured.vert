#version 120
#extension all : disable

attribute vec2 the_tex_coords;

uniform vec3 translation;
uniform mat4 transformation;

varying vec2 tex_coords;

#if (__VERSION__ > 120)
in vec4 gl_Vertex;
#endif

void main ()
{
  gl_Position = transformation * (vec4(translation, 0.0) + gl_Vertex);

  tex_coords = the_tex_coords;
} 
