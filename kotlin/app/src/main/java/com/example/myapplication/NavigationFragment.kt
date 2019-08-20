package com.example.myapplication

import android.content.SharedPreferences
import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import kotlinx.android.synthetic.main.login_fragment.view.*
import kotlinx.android.synthetic.main.navigation_fragment.view.*
import okhttp3.OkHttpClient
import org.jetbrains.anko.AnkoLogger
import org.jetbrains.anko.doAsync
import org.jetbrains.anko.info
import org.jetbrains.anko.uiThread
import org.json.JSONArray

class NavigationFragment : Fragment() {

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view = inflater.inflate(R.layout.navigation_fragment, container, false)

        view.join_events_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(joinEventsFragment(), false) })

        view.event_venue_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(eventAtVenueFragment(), false) })

        view.free_venues_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(freeVenueFragment(), false) })

        view.free_times_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(freeTimeFragment(), false) })

        view.events_in_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(eventsInFragment(), false) })

        view.logout_button.setOnClickListener({
            (activity as NavigationHost).navigateTo(LoginFragment(), false) })
        return view
    }

}