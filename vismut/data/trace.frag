#version 120
#extension GL_all : disable

uniform sampler1D color_map;

in float color_index;

void main ()
{
  gl_FragColor = texture1D(color_map, color_index);
}
