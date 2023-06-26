package com.example.smartwardrobe.ui.home

import android.Manifest

import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Address
import android.location.LocationManager
import android.location.LocationManager.*
import android.opengl.Visibility
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.lifecycleScope
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.smartwardrobe.MainActivity
import com.example.smartwardrobe.R
import com.example.smartwardrobe.RetrofitClient
import com.example.smartwardrobe.data.ClothingItem
import com.example.smartwardrobe.data.model.Outfit
import com.example.smartwardrobe.databinding.FragmentHomeBinding
import com.example.smartwardrobe.rate.RateActivity
import com.example.smartwardrobe.ui.closet.ClothingAdapter
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private lateinit var locationManager: LocationManager
    lateinit var outfit: Outfit
    private lateinit var itemsAdapter: OutfitAdapter


    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View {
        val homeViewModel =
            ViewModelProvider(this).get(HomeViewModel::class.java)

        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val root: View = binding.root
        binding.btnRegenerate.visibility = View.GONE
//        binding.btnNewOutfit.text = getString(R.string.regenerate_outfit)

        locationManager = requireActivity().getSystemService(Context.LOCATION_SERVICE) as LocationManager
//        outfit = ArrayList<ClothingItem>()
        binding.outfit.layoutManager = LinearLayoutManager(activity)

        itemsAdapter = OutfitAdapter()
        binding.outfit.adapter = itemsAdapter

        //remove this:
        binding.btnRate.setOnClickListener {

            val intent = Intent(activity, RateActivity::class.java)
            val extraData = "5"//outfit id
            intent.putExtra("outfit_id", outfit.outfitId)
            intent.putExtra("user_id", outfit.userId)
            startActivity(intent)
        }


        binding.btnRegenerate.setOnClickListener {
            (activity as MainActivity?)?.getLocation { addressList ->
                // Handle the geocoding result here
                if (addressList != null) {
                    Toast.makeText(context, addressList?.get(0)?.locality ?: "non", Toast.LENGTH_LONG).show()
                    lifecycleScope.launch {
                        val clothingLst = regenerate(outfit.outfitId, addressList)
                        if (clothingLst != null) {
                            outfit = clothingLst
                            val newItems: ArrayList<ClothingItem> = clothingLst.list
                            itemsAdapter.updateData(newItems)

                            itemsAdapter.notifyDataSetChanged()

                        } else {
                            //there was an error generating the outfit todo
                        }
                    }
                } else {
                    Toast.makeText(context, addressList?.get(0)?.locality ?: "non", Toast.LENGTH_LONG).show()
                }
            }
        }
        binding.btnNewOutfit.setOnClickListener {
            (activity as MainActivity?)?.getLocation { addressList ->
                // Handle the geocoding result here
                if (addressList != null) {
                    Toast.makeText(context, addressList?.get(0)?.locality ?: "non", Toast.LENGTH_LONG).show()
                    lifecycleScope.launch {
                        val clothingLst = getOutfit(addressList)
                        if (clothingLst != null) {
                            outfit = clothingLst
                            val newItems: ArrayList<ClothingItem> = clothingLst.list
                            itemsAdapter.updateData(newItems)

                            itemsAdapter.notifyDataSetChanged()
                            binding.btnRegenerate.visibility = View.VISIBLE
                            binding.btnRate.visibility = View.VISIBLE
                            binding.btnNewOutfit.visibility = View.GONE
                        } else {
                            //there was an error generating the outfit todo
                        }
                    }
//                    outfit = getOutfit(addressList)
                } else {
                    Toast.makeText(context, addressList?.get(0)?.locality ?: "non", Toast.LENGTH_LONG).show()
                }
            }

//            var addressList: List<Address>? = (activity as MainActivity?)?.getLocation()
//            Toast.makeText(context, addressList?.get(0)?.locality ?: "non", Toast.LENGTH_LONG).show()
//            (activity as MainActivity?)?.getLocation()
//            var outfit = getOutfit(addressList)

        }
        return root
    }

    private suspend fun regenerate(outfitId: Int, addressList: List<Address>?): Outfit? {
        var retrofit = RetrofitClient.myApi
        val queryParameters =
            mapOf(
                "id" to (activity as MainActivity).userid,
                "latitude" to addressList!![0].latitude.toString(),
                "longitude" to addressList!![0].longitude.toString(),
                "outfitid" to outfitId.toString()
            )

        return withContext(Dispatchers.IO) {
            try {
                val response = retrofit.regenerateOutfit(queryParameters).execute()
                if (response.isSuccessful) {
                    val lst = response.body()
                    lst // Cast the response to Outfit
                } else {
                    null // Return null or handle the error case appropriately
                }
            } catch (e: Exception) {
                print(e)
                null // Return null or handle the exception case appropriately
            }
        }
    }

    private suspend fun getOutfit(addressList: List<Address>?): Outfit? {
        val out: Outfit
        var retrofit = RetrofitClient.myApi
        val queryParameters = mapOf("id" to (activity as MainActivity).userid, "latitude" to addressList!![0].latitude.toString(), "longitude" to addressList!![0].longitude.toString())

        return withContext(Dispatchers.IO) {
            try {
                val response = retrofit.getOutfit(queryParameters).execute()
                if (response.isSuccessful) {
                    val lst = response.body()
                    lst // Cast the response to Outfit
                } else {
                    null // Return null or handle the error case appropriately
                }
            } catch (e: Exception) {
                print(e)
                null // Return null or handle the exception case appropriately
            }
        }
    }/*
        GlobalScope.launch(Dispatchers.IO) {
            val response = retrofit.getOutfit(queryParameters as Map<String, String>).execute()
            withContext(Dispatchers.Main) {
                if (response.isSuccessful) {
                    val data = response.body()
                    // Do something with the data
                } else {
                    // Handle error
                }
            }
        }
        return null
    }*/


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        if (ActivityCompat.checkSelfPermission(requireContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(requireActivity(), arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), MainActivity.REQUEST_CODE_LOCATION_PERMISSION)

            /* val location: Location? = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER)
         if (location != null) {
             // Use location.latitude and location.longitude to get the latitude and longitude values.
             Log.d("Location", "Latitude: ${location.latitude}, Longitude: ${location.longitude}")
         }*/
        }
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == MainActivity.REQUEST_CODE_LOCATION_PERMISSION) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permission granted, handle location retrieval here
            } else {
                // Permission denied, handle accordingly (e.g. show a message to the user)
            }
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}