#version 130
#extension all : disable

#if (__VERSION__ > 120)
in vec4 gl_Vertex;
#endif

in unsigned short arrow_id;

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

  color_index = float(arrows) / float(arrow_id);
} 
