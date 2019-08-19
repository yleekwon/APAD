package com.example.myapplication

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.free_venue_fragment.view.*
import kotlinx.android.synthetic.main.navigation_fragment.view.*
import org.jetbrains.anko.doAsync
import org.json.JSONArray
import org.json.JSONObject
import org.jetbrains.anko.activityUiThread
import com.squareup.okhttp.OkHttpClient
import com.squareup.okhttp.Request
import kotlinx.android.synthetic.main.free_venue_fragment.*
import org.jetbrains.anko.uiThread



class freeVenueFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.free_venue_fragment, container, false)

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

                        if(user.get("timeslot") == txtsearchuser.text.toString()) {
                            println("wtf")
                            (if(user.get("event_id").toString() == "empty"){
                                println("wtf1")
                                //txtusername.text = user.get("venue_id").toString()
                                var x = user.get("venue_id").toString()
                                myList.add(x)
                                println(myList)
                            })
                            val venueList = mutableListOf<String>()
                            for (i in 0..(jsonarray2.length() - 1)) {
                                val venue = jsonarray2.getJSONObject(i)
                                if(venue.get("venue_id").toString() in myList){
                                    var ven = venue.get("bldg_code").toString()
                                    var ven1 = venue.get("floor_num").toString()
                                    var ven2 = venue.get("room_num").toString()
                                    var ven3 = ("%s %s.%s \n".format(ven, ven1, ven2))
                                    venueList.add(ven3)
                                }
                            }
                            txtusername.text = venueList.toString().replace(",", "")  //remove the commas
                                .replace("[", "")  //remove the right bracket
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