#version 120
#extension GL_all : disable

#if (__VERSION__ > 120)
out vec4 gl_FragColor;
#endif

uniform sampler1D color_map;

#if (__VERSION__ <= 120)
varying float color_index;
#else
in float color_index;
#endif

void main ()
{
#if (__VERSION__ <= 120)
  gl_FragColor = texture1D(color_map, color_index);
#else
  gl_FragColor = texture(color_map, color_index);
#endif
}
