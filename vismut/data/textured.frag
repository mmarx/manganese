#version 120
#extension GL_all : disable

uniform sampler2D the_texture;

varying vec2 tex_coords;

void main ()
{
  gl_FragColor = texture2D(the_texture, tex_coords);
}
