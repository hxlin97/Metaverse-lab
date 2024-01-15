using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rungrid : MonoBehaviour
{
    public GridMeshCreate gridMeshCreate;

    private void Start()
    {
        Run();
    }

    private void Run()
    {
        //gridMeshCreate.gridEvent = GridEvent;
        gridMeshCreate.CreateMesh();
    }

    private void GridEvent(Grid grid)
    {
        grid.color = Color.red;
        grid.Onclick = () =>
        {
            grid.color = Color.blue;
        };
    }
}
