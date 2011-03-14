#version 120
#extension all : disable

uniform mat4 transformation;

#if (__VERSION__ > 120)
in vec3 vertex;
#endif

void main ()
{
#if (__VERSION__ <= 120)
  gl_Position = transformation * gl_Vertex;
#else
  gl_Position = transformation * vertex;
#endif

  gl_PointSize = 25;
} 
