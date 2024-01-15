using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class GridMeshCreate : MonoBehaviour
{
    [Serializable]
    public class MeshRange {
        public int width;
        public int height;

    }

    public MeshRange meshrange;
    public Vector3 startpos;
    public Transform parentTran;
    public GameObject gridPre;

    public Vector2 scale;

    private GameObject[,] m_grids;
    public GameObject[,] grids {
        get {
            return m_grids;
        }
    }

    public Action<GameObject, int, int> gridEvent;
    public void CreateMesh() 
    {
        if (meshrange.width == 0 || meshrange.height == 0)
        {
            return;    
        }
        ClearMesh();
        m_grids = new GameObject[meshrange.width, meshrange.height];
        for (int i = 0; i < meshrange.width; i++)
        {
            for (int j = 0; j < meshrange.height; j++)
            {
                CreateGrid(i, j);   
            }
        }
    }

    public void CreateMesh(int height, int width)
    {
        if (width == 0 || height == 0)
        {
            return;
        }
        ClearMesh();
        m_grids = new GameObject[width, height];
        for (int i = 0; i < width; i++)
        {
            for (int j = 0; j < height; j++)
            {
                CreateGrid(i, j);
            }
        }
    }

    public void CreateGrid(int row, int column)
    {
        GameObject go = GameObject.Instantiate(gridPre, parentTran);
        //Grid grid = go.GetComponent<Grid>();
        float posY = startpos.y + scale.y * row;
        float posX = startpos.x + scale.x * column;
        go.transform.position = new Vector3(posX, posY, startpos.z);
        m_grids[row, column] = go;
        gridEvent?.Invoke(go,row, column);

    }

    public void ClearMesh()
    {
        if (m_grids == null || m_grids.Length == 0)
        {
            return;
        }
        foreach (GameObject go in m_grids)
        {
            if (go != null)
            {
                Destroy(go);
            }
        }
        Array.Clear(m_grids, 0, m_grids.Length);
    }
}
