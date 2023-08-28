using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ChronoText : MonoBehaviour
{
	private GameMaster gm;
	//private GameObject checkPoint;
	private Text text;
	public float theTime;
	private bool timeOn = false;

	public Color timeColor;
	public Color slowColor;
	public float speed = 1;


    // Start is called before the first frame update
    void Start()
    {		
		gm = GameObject.FindGameObjectWithTag("GM").GetComponent<GameMaster>();
		text = GetComponent<Text>();
		//text.text = gm.lastTime;
		//theTime = gm.lastTimeCount;
		timeOn = true;
    }

    // Update is called once per frame
    void Update()
    {
		var moveScript = GameObject.FindGameObjectWithTag("Player").GetComponent<PlayerMove>();
		if(moveScript.speed <= moveScript.intialSpeed) 
		{
			speed = 1;
			text.color = new Color(0f,0.4901961f,1f);
		}
		else
		{
			speed = 0.5f;
			text.color = Color.white;
		}
		if (timeOn){
			theTime = gm.lastTimeCount += (Time.deltaTime * speed);

			string minutes = Mathf.Floor((theTime % 3600)/60).ToString("00");
			string miliseconds = (theTime % 60).ToString("F2");
			text.text = minutes + ":" + miliseconds;
		}
    }
}
