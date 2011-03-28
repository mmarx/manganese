#version 120
#extension GL_all : disable

uniform sampler2D texture;

in vec2 the_tex_coords;

void main ()
{
  gl_FragColor = texture2D(texture, the_tex_coords);
}
