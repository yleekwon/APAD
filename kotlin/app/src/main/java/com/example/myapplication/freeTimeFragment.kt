package com.example.myapplication

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.free_time_fragment.*
import kotlinx.android.synthetic.main.free_time_fragment.view.*
import kotlinx.android.synthetic.main.navigation_fragment.view.*
import okhttp3.OkHttpClient
import okhttp3.Request
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.uiThread
import org.json.JSONArray

class freeTimeFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.free_time_fragment, container, false)

        view.back_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(NavigationFragment(), false) })

        view.button.setOnClickListener {
            doAsync {
                println("this should werk")
                val gotresponse = fetchInfo()
                val gotresponse2 = fetchInfo2()
                println("maybe?")
                val jsonarray = JSONArray(gotresponse)
                val jsonarray2 = JSONArray(gotresponse2)

                println("how bout now")
                uiThread {
                    //iterate through the returned array of JSON objects
                    // and look for candiadate whose name we requested
                    println("here?")
                    val myList = mutableListOf<String>()
                    for (i in 0..(jsonarray.length() - 1)) {
                        val user = jsonarray.getJSONObject(i)
                        if(user.get("venue_id").toString() == txtsearchuser.text.toString()) {
                            println("wtf")
                            (if (user.get("event_id").toString() == "empty") {
                                println("wtf1")
                                var x = user.get("timeslot").toString()
                                myList.add(x)
                                println(myList)
                                //txtusername.text = user.get("timeslot").toString()
                            })

                            txtusername.text = myList.toString().replace("[", "")  //remove the right bracket
                                .replace("]", "")  //remove the left bracket
                        }
                    }
                }
            }
        }

        return view;
    }
    private fun fetchInfo(): String {
        val url = "https://comehither.appspot.com/timetable"

        val client = OkHttpClient()
        println("hi")
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .build()
        println("hello")
        val response = client.newCall(request).execute()
        println("pls")
        val bodystr =  response.body().string() // this can be consumed only once

        return bodystr
    }
    private fun fetchInfo2(): String {
        val url = "https://comehither.appspot.com/venuetable"

        val client = OkHttpClient()
        println("hi")
        val request = Request.Builder()
            .url(url)
            .header("User-Agent", "Android")
            .build()
        println("hello")
        val response = client.newCall(request).execute()
        println("pls")
        val bodystr =  response.body().string() // this can be consumed only once

        return bodystr
    }

}


