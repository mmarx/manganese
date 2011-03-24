#version 120
#extension GL_all : disable

uniform vec4 color;
uniform sampler2D texture0;

varying vec2 tex_coords;

void main ()
{
  vec4 texel;

  texel = texture2D(texture0, tex_coords);
  gl_FragColor = mix(color, vec4(texel.rgb, 1.0), texel.a);
}
