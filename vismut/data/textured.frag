#version 120
#extension GL_all : disable

uniform sampler2D texture;

#if (__VERSION__ <= 120)
varying vec2 the_tex_coords;
#else
in vec2 the_tex_coords;
#endif

void main ()
{
  gl_FragColor = texture2D(texture, the_tex_coords);
}
