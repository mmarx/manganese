#version 120
#extension GL_all : disable

varying vec4 the_color;

void main ()
{
  gl_FragColor = the_color;
}
