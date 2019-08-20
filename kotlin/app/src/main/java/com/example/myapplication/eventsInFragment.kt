package com.example.myapplication

import android.content.SharedPreferences
import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.events_in_fragment.*
import kotlinx.android.synthetic.main.events_in_fragment.view.*
import okhttp3.MediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody
import org.jetbrains.anko.AnkoLogger
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info
import org.jetbrains.anko.uiThread
import org.jetbrains.anko.activityUiThread
import org.json.JSONArray

class eventsInFragment : Fragment(){

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {

        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.events_in_fragment, container, false)

        view.back_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(NavigationFragment(), false)
        })
        view.button.setOnClickListener {
            doAsync {
                val gotresponse = fetchInfos()
                val gotresponse2 = fetchInfos2()
                val gotresponse3 = fetchInfos3()
                val jsonarray = JSONArray(gotresponse)
                val jsonarray2 = JSONArray(gotresponse2)
                val jsonarray3 = JSONArray(gotresponse3)

                uiThread {
                    val myList = mutableListOf<String>()
                    for (i in 0..(jsonarray3.length() - 1)) {
                        val id = jsonarray3.getJSONObject(i)
                        if (id.get("EID").toString() == txtsearchuser.text.toString()){
                            var eid = id.get("user_id").toString()
                            for (i in 0..(jsonarray.length() - 1)) {
                                val user = jsonarray.getJSONObject(i)
                                if (user.get("user_id").toString() == eid) {
                                    println("wtf")
                                    var x = user.get("event_id").toString()
                                    myList.add(x)
                                    println(myList)
                                    val eventList = mutableListOf<String>()
                                    for (i in 0..(jsonarray2.length() - 1)) {
                                        val venue = jsonarray2.getJSONObject(i)
                                        if (venue.get("event_id").toString() in myList) {
                                            var ven = venue.get("name").toString()
                                            var ven1 = venue.get("description").toString()
                                            var ven3 = ("%s: %s \n".format(ven, ven1))
                                            eventList.add(ven3)
                                        }
                                    }

                                    txtusername.text = eventList.toString().replace(",", "")  //remove the commas
                                        .replace("[", "")  //remove the right bracket
                                        .replace("]", "")  //remove the left bracket
                                }
                            }
                        }
                    }
                }
            }
        }
        return view
    }
private fun fetchInfos(): String {
    val url = "https://comehither.appspot.com/confirmedtable"

    val client = com.squareup.okhttp.OkHttpClient()
    val request = com.squareup.okhttp.Request.Builder()
        .url(url)
        .header("User-Agent", "Android")
        .build()
    val response = client.newCall(request).execute()
    val bodystr =  response.body().string() // this can be consumed only once

    return bodystr
}

private fun fetchInfos2(): String {
    val url = "https://comehither.appspot.com/eventtable"

    val client = com.squareup.okhttp.OkHttpClient()
    val request = com.squareup.okhttp.Request.Builder()
        .url(url)
        .header("User-Agent", "Android")
        .build()
    val response = client.newCall(request).execute()
    val bodystr =  response.body().string() // this can be consumed only once

    return bodystr
}
private fun fetchInfos3(): String {
    val url = "https://comehither.appspot.com/usertable"

    val client = com.squareup.okhttp.OkHttpClient()
    val request = com.squareup.okhttp.Request.Builder()
        .url(url)
        .header("User-Agent", "Android")
        .build()
    val response = client.newCall(request).execute()
    val bodystr =  response.body().string() // this can be consumed only once

    return bodystr
}

}