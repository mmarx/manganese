uniform mat4 transformation;

void main ()
{
  gl_Position = transformation * gl_Vertex;
  gl_PointSize = 25;
} 
