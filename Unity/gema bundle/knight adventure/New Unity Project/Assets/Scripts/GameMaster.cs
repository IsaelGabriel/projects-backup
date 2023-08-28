using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameMaster : MonoBehaviour
{
	private static GameMaster instance;
	public Vector3 lastCheckpointPos;
	//public string lastTime;
	public float lastTimeCount;
	public int timesPlayed;
	//public bool checkpointSaved;
	public int lastLives = 2;
	void Awake(){

		if(instance == null){
			instance = this;
			DontDestroyOnLoad(instance);
		}
		else
		{
			Destroy(gameObject);
		}
	}
}
