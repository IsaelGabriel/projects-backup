using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ChecpointScript : MonoBehaviour
{
	private GameMaster gm;
	private Text timerText;
	private bool collidedWithPlayer;
	private bool alreadySaved = false;
	public int playedCount;
	//private var scriptTime;
	//private Vector3 checkPos = (transform.position.x, transform.position.y, transform.position.z);
	//private var playerValues;

	void Start(){
		gm = GameObject.FindGameObjectWithTag("GM").GetComponent<GameMaster>();
		timerText = GameObject.Find("TimerText").GetComponent<Text>();
		//scriptTime = GameObject.Find("TimerText").GetComponent<ChronoText>();
		if(gm.lastCheckpointPos == gameObject.transform.position)
		{
			if(!alreadySaved)
			{
				alreadySaved = true;
			}
		}
	//	gm.timesPlayed = playedCount + 1;
	//	playedCount = gm.timesPlayed;
	}

	void Update()
	{
		if(gm.lastCheckpointPos == gameObject.transform.position)
		{
			if(!alreadySaved)
			{
				alreadySaved = true;
			}
		}
	}

	void OnTriggerEnter(Collider collider){
		if(collider.gameObject.tag == "Player")
		{
			var playerValues = collider.GetComponent<PlayerHealth>();

			if(!alreadySaved)
			{
				var scriptTime = GameObject.Find("TimerText").GetComponent<ChronoText>();
				gm.lastCheckpointPos = transform.position;
				//gm.lastTime = timerText.text;
				gm.lastTimeCount = scriptTime.theTime;
				gm.lastLives = playerValues.lives;
			}
			else
			{
				gm.lastLives = playerValues.lives;
			}
		}
	}
}
