#version 120
#extension all : disable

#if (__VERSION__ > 120)
in vec4 gl_Vertex;
#endif

#if (__VERSION__ <= 120)
attribute float arrow_id;
#else
in float arrow_id;
#endif

uniform int arrows;
uniform mat4 transformation;

#if (__VERSION__ <= 120)
varying float color_index;
#else
out float color_index;
#endif

void main ()
{
  gl_Position = transformation * gl_Vertex;

  color_index = arrow_id / float(arrows);
} 
