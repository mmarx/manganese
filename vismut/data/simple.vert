#version 120
#extension all : disable

uniform mat4 transformation;

#if (__VERSION__ > 120)
in vec4 gl_Vertex;
#endif

void main ()
{
  gl_Position = transformation * gl_Vertex;
  gl_PointSize = 25;
} 
