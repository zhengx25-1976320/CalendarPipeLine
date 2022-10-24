package com.example.calendarpipeline;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ListView;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.text.ParseException;
import java.util.ArrayList;
import android.widget.Switch;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class Shopping extends AppCompatActivity {

    ListView listView;
    ArrayList<itemModel> arrayList;
    ArrayList<itemModel2> arrayList2;
    boolean is_by_price;
    Switch byprice;
    EditText searchQuery;
    Button searchButton;
    TextView title;
    String message;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_shopping);
        byprice = (Switch) this.findViewById(R.id.bypriceswitch);

        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }


//        searchQuery = (EditText) this.findViewById(R.id.search_query);
//        searchButton = (Button) this.findViewById(R.id.search_button);
        Intent intent = getIntent();
        message = intent.getStringExtra(MainActivity.EXTRA_MESSAGE);
//        searchQuery.setText(message);
//        System.out.println(searchButton);

        System.out.println(message.toString());


        Python py = Python.getInstance();
        PyObject pyObj = py.getModule("GetItem");
//                PyObject obj = pyObj.callAttr("printItem", searchQuery.getText().toString());
//                PyObject objAmz = pyObj.callAttr("get_amazon_results");
        PyObject objAmz = pyObj.callAttr("get_amazon_results", message.toString());
        PyObject objEbay = pyObj.callAttr("get_ebay_results", message.toString());


        listView = (ListView) findViewById(R.id.jsonListView);
        arrayList = new ArrayList<>();

        try {
//                        JSONObject object = new JSONObject(readJSON(getFilesDir() + "/" + "json_1_all_info_dict"));
            JSONObject object = new JSONObject(readJSON("json_1_all_info_dict.json"));
            for (int i = 0; i < object.names().length(); i++) {
                System.out.println(object.names().getString(i));
                JSONObject jsonObject = (JSONObject) object.get(object.names().getString(i));
                String site = jsonObject.getString("site");
                String price = jsonObject.getString("price");
                String rating = jsonObject.getString("rating");
                String reviews = jsonObject.getString("reviews");
                String title = jsonObject.getString("title");
//                        String searchurl = jsonObject.getString("search_url");
                String url = jsonObject.getString("url");
                String image = jsonObject.getString("image");
                String reviewLink = jsonObject.getString("reviewLink");
                itemModel model = new itemModel();

                model.setSite(site);
                model.setPrice(price);
                model.setRating(rating);
                model.setReviews(reviews);
                model.setTitle(title);
//                        model.setSearch_url(searchurl);
                model.setUrl(url);
                model.setImage(image);
                model.setReviewLink(reviewLink);

                arrayList.add(model);
            }
        } catch (JSONException e) {
            e.printStackTrace();
        }
        CustomAdapter adapter = new CustomAdapter(Shopping.this, arrayList);
        listView.setAdapter(adapter);











//        searchButton.setOnClickListener(new View.OnClickListener() {
//            public void onClick(View v) {
//                // Do something in response to button click
//                System.out.println(searchQuery.getText().toString());
//                Python py = Python.getInstance();
//                PyObject pyObj = py.getModule("GetItem");
////                PyObject obj = pyObj.callAttr("printItem", searchQuery.getText().toString());
////                PyObject objAmz = pyObj.callAttr("get_amazon_results");
//                PyObject objAmz = pyObj.callAttr("get_amazon_results", searchQuery.getText().toString());
//                PyObject objEbay = pyObj.callAttr("get_ebay_results", searchQuery.getText().toString());
//
//
//                listView = (ListView) findViewById(R.id.jsonListView);
//                arrayList = new ArrayList<>();
//
//                try {
////                        JSONObject object = new JSONObject(readJSON(getFilesDir() + "/" + "json_1_all_info_dict"));
//                    JSONObject object = new JSONObject(readJSON("json_1_all_info_dict.json"));
//                    for (int i = 0; i < object.names().length(); i++) {
//                        System.out.println(object.names().getString(i));
//                        JSONObject jsonObject = (JSONObject) object.get(object.names().getString(i));
//                        String site = jsonObject.getString("site");
//                        String price = jsonObject.getString("price");
//                        String rating = jsonObject.getString("rating");
//                        String reviews = jsonObject.getString("reviews");
//                        String title = jsonObject.getString("title");
////                        String searchurl = jsonObject.getString("search_url");
//                        String url = jsonObject.getString("url");
//                        String image = jsonObject.getString("image");
//                        String reviewLink = jsonObject.getString("reviewLink");
//                        itemModel model = new itemModel();
//
//                        model.setSite(site);
//                        model.setPrice(price);
//                        model.setRating(rating);
//                        model.setReviews(reviews);
//                        model.setTitle(title);
////                        model.setSearch_url(searchurl);
//                        model.setUrl(url);
//                        model.setImage(image);
//                        model.setReviewLink(reviewLink);
//
//                        arrayList.add(model);
//                    }
//                } catch (JSONException e) {
//                    e.printStackTrace();
//                }
//                CustomAdapter adapter = new CustomAdapter(Shopping.this, arrayList);
//                listView.setAdapter(adapter);
//
//
//            }
//        });


//        android:id="@+id/title"
//        title = (TextView)findViewById(R.id.title);
//        title.setOnClickListener(new View.OnClickListener() {
//            public void onClick(View v) {
//                System.out.println("check this out");
//            }
//        });


        byprice.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if (b) {
                    listView = (ListView) findViewById(R.id.jsonListView);
                    arrayList2 = new ArrayList<>();

//                    Python py = Python.getInstance();
//                    PyObject pyObj = py.getModule("GetItem");
//                    String testtt = "aa";
//                    PyObject obj = pyObj.callAttr("printItem", testtt);
//                    PyObject objAmz = pyObj.callAttr("get_amazon_results");


//                    System.out.println(String.valueOf("this is the object" + obj));

//                    File json1 = new File(getFilesDir() + "/" + "json_1_all_info_dict");
//                    File file = new File(getFilesDir(), "json_1_all_info_dict");
//                    FileReader fileReader = new FileReader(file);
//                    openFileInput
//                    InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
//                    BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
//                    String receiveString = "";
//                    StringBuilder stringBuilder = new StringBuilder();
//                    BufferedReader bufferedReader = new BufferedReader(fileReader);
//                    StringBuilder stringBuilder = new StringBuilder();
//                    String line = bufferedReader.readLine();
//                    while (line != null){
//                        stringBuilder.append(line).append("\n");
//                        line = bufferedReader.readLine();
//                    }
//                    bufferedReader.close();
//// This responce will have Json Format String
//                    String responce = stringBuilder.toString();

//                    System.out.println("hii" + file);


                    try {
                        JSONObject object = new JSONObject(readJSON("json_2_all_price_sort_dict.json"));
                        for (int i = 0; i < object.names().length(); i++) {
                            System.out.println(object.names().getString(i));
                            JSONObject jsonObject = (JSONObject) object.get(object.names().getString(i));
                            String site = jsonObject.getString("site");
                            String price = jsonObject.getString("price");
                            String rating = jsonObject.getString("rating");
                            String reviews = jsonObject.getString("reviews");
                            String title = jsonObject.getString("title");
//                        String searchurl = jsonObject.getString("search_url");
                            String url = jsonObject.getString("url");
                            String image = jsonObject.getString("image");
                            String reviewLink = jsonObject.getString("reviewLink");
                            itemModel2 model = new itemModel2();


                            model.setSite(site);
                            model.setPrice(price);
                            model.setRating(rating);
                            model.setReviews(reviews);
                            model.setTitle(title);
//                        model.setSearch_url(searchurl);
                            model.setUrl(url);
                            model.setImage(image);
                            model.setReviewLink(reviewLink);

                            arrayList2.add(model);

                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    CustomAdapter2 adapter = new CustomAdapter2(Shopping.this, arrayList2);
                    listView.setAdapter(adapter);
                } else {

                    listView = (ListView) findViewById(R.id.jsonListView);
                    arrayList = new ArrayList<>();

                    try {
                        JSONObject object = new JSONObject(readJSON("json_1_all_info_dict.json"));
                        for (int i = 0; i < object.names().length(); i++) {
                            System.out.println(object.names().getString(i));
                            JSONObject jsonObject = (JSONObject) object.get(object.names().getString(i));
                            String site = jsonObject.getString("site");
                            String price = jsonObject.getString("price");
                            String rating = jsonObject.getString("rating");
                            String reviews = jsonObject.getString("reviews");
                            String title = jsonObject.getString("title");
//                        String searchurl = jsonObject.getString("search_url");
                            String url = jsonObject.getString("url");
                            String image = jsonObject.getString("image");
                            String reviewLink = jsonObject.getString("reviewLink");
                            itemModel model = new itemModel();

                            model.setSite(site);
                            model.setPrice(price);
                            model.setRating(rating);
                            model.setReviews(reviews);
                            model.setTitle(title);
//                        model.setSearch_url(searchurl);
                            model.setUrl(url);
                            model.setImage(image);
                            model.setReviewLink(reviewLink);

                            arrayList.add(model);
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    CustomAdapter adapter = new CustomAdapter(Shopping.this, arrayList);
                    listView.setAdapter(adapter);
                }
            }
        });
    }

    public String readJSON(String filename) {
        String json = null;
        try {
            // Opening data.json file
            InputStream inputStream;
            inputStream = openFileInput(filename);
//            inputStream = getAssets().open(filename);

            int size = inputStream.available();
            byte[] buffer = new byte[size];
            // read values in the byte array
            inputStream.read(buffer);
            inputStream.close();
            // convert byte to string
            json = new String(buffer, "UTF-8");
        } catch (IOException e) {
            e.printStackTrace();
            return json;
        }
        return json;
    }
}
