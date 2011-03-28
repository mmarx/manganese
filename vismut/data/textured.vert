#version 120
#extension all : disable

#if (__VERSION__ > 120)
in vec4 gl_Vertex;
#endif

in vec2 tex_coords;

uniform vec3 translation;
uniform mat4 transformation;

#if (__VERSION__ <= 120)
varying vec2 the_tex_coords;
#else
out vec2 the_tex_coords;
#endif

void main ()
{
  gl_Position = transformation * (vec4(translation, 0.0) + gl_Vertex);

  the_tex_coords = tex_coords;
} 
