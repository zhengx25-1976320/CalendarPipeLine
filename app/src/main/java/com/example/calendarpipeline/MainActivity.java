package com.example.calendarpipeline;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.StrictMode;
import android.provider.CalendarContract;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.text.InputType;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.TimeZone;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.os.Looper;
import android.provider.Settings;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;

public class MainActivity extends AppCompatActivity implements TextToSpeech.OnInitListener{

    public static final Integer RecordAudioRequestCode = 1;
    public static final Integer callbackId = 42;
    private EditText startDateText;
    private EditText startTimeText;
    private EditText endDateText;
    private EditText endTimeText;
    private EditText eventNameText;
    private EditText eventDurationText;
    private Button show_button;
    private Button write_button;
    private TextView showSlot;
    private ImageView micButton;
    private String[] queryStartDate;
    private String[] queryEndDate;
    private String[] queryStartTime;
    private String[] queryEndTime;
    private String name;
    private String location;
    private long startUnixTime;
    private long endUnixTime;
    private long eventDuration;
    private long eventStartTime;
    private long eventEndTime;
    private boolean con;
    private ArrayList<CalendarDataStruct> eventList;
    private SpeechRecognizer speechRecognizer;
    private TextToSpeech textToSpeech;
    private String bool;
    private String noun_phrase;
    private double latitudeTextView;
    private double longitTextView;
    private String des;
    private boolean availableOrNot;
    private String code;
    FusedLocationProviderClient mFusedLocationClient;
    public static final String EXTRA_MESSAGE = "com.example.calendarpipline.MESSAGE";
    String date;

    // Initializing other items
    // from layout file
//    TextView latitudeTextView, longitTextView;
    int PERMISSION_ID = 44;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);

        // method to get the location
        getLastLocation();
        StrictMode.setVmPolicy(new StrictMode.VmPolicy.Builder(StrictMode.getVmPolicy())
                .detectLeakedClosableObjects()
                .build());
        textToSpeech = new TextToSpeech(this, this);

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            checkRecordPermission();
        }

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_CALENDAR) != PackageManager.PERMISSION_GRANTED) {
            checkCalendarPermission(callbackId, Manifest.permission.READ_CALENDAR, Manifest.permission.WRITE_CALENDAR);
        }

        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

//        startDateText = (EditText)findViewById(R.id.start_date_input);
//        startTimeText = (EditText)findViewById(R.id.start_time_input);
//        endDateText = (EditText)findViewById(R.id.end_date_input);
//        endTimeText = (EditText)findViewById(R.id.end_time_input);
//        eventNameText = (EditText)findViewById(R.id.event_name_input);
//        eventDurationText = (EditText)findViewById(R.id.event_duration_input);
//        showSlot = (TextView)findViewById(R.id.time_slot);
//        startDateText.setRawInputType(InputType.TYPE_CLASS_NUMBER);
//        startTimeText.setRawInputType(InputType.TYPE_CLASS_NUMBER);
//        endDateText.setRawInputType(InputType.TYPE_CLASS_NUMBER);
//        endTimeText.setRawInputType(InputType.TYPE_CLASS_NUMBER);
//        show_button = (Button)findViewById(R.id.show_button);
//        write_button = (Button)findViewById((R.id.write_button));
        micButton = findViewById(R.id.mic_button);
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        final Intent speechRecognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());

//        latitudeTextView = findViewById(R.id.latTextView);
//        longitTextView = findViewById(R.id.lonTextView);

        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);




        micButton.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View view, MotionEvent motionEvent) {
                if (motionEvent.getAction() == MotionEvent.ACTION_UP){
                    micButton.setImageResource(R.drawable.ic_mic_black_off);
                    speechRecognizer.stopListening();
                }
                if (motionEvent.getAction() == MotionEvent.ACTION_DOWN){
                    micButton.setImageResource(R.drawable.ic_mic_black_24dp);
                    speechRecognizer.startListening(speechRecognizerIntent);
                }
                return false;
            }
        });

        speechRecognizer.setRecognitionListener(new RecognitionListener() {
            @Override
            public void onReadyForSpeech(Bundle bundle) {

            }

            @Override
            public void onBeginningOfSpeech() {

            }

            @Override
            public void onRmsChanged(float v) {

            }

            @Override
            public void onBufferReceived(byte[] bytes) {

            }

            @Override
            public void onEndOfSpeech() {

            }

            @Override
            public void onError(int i) {

            }

            @Override
            public void onResults(Bundle bundle) {
                ArrayList<String> data = bundle.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                System.out.println(data);
//                String speechText = data.toString();
                String speechText = data.get(0);
                Python py = Python.getInstance();
                Python py_search = Python.getInstance();
//
//                PyObject pyObj = py.getModule("new0801");
                PyObject pyObj = py.getModule("10-12");
                PyObject searchObj = py_search.getModule("search_python");
                PyObject convertObj = py.getModule("convert_zip_code");
                PyObject testOBJ = py.getModule("duplicate");
                PyObject test_res = testOBJ.callAttr("assign_task", speechText);
                String out = String.valueOf(test_res.asList().get(0));
                System.out.println(out);
                System.out.println(test_res.asList());
                if (out.equals("calendar")) {
                    System.out.println("calendar module");
                    try {
//                    PyObject obj = pyObj.callAttr("main", speechText);
                        PyObject obj = pyObj.callAttr("text_to_event", speechText);
                        name = String.valueOf(obj.asMap().get("event subject"));
//                    eventDuration = Long.parseLong(String.valueOf(obj.asMap().get("duration")));
//                    eventStartTime = (long)Double.parseDouble(String.valueOf(obj.asMap().get("time")));

                        eventStartTime = (long)Double.parseDouble(String.valueOf(obj.asMap().get("start date")));
                        System.out.println(eventStartTime);
//                    startUnixTime = eventStartTime;
//                    endUnixTime = eventStartTime + 4 * 60 * 1000;
                        System.out.println(name);
//                    System.out.println(eventDuration);
//                    System.out.println(eventStartTime);
//                System.out.println(eventStartTime);
//                    calculateEventStartTime();calculateValidTime();
//                    writeToCalender();
//                    texttoSpeak();

                    } catch(Exception e) {
                        Toast myToast = Toast.makeText(getApplicationContext(), "Sorry, we didn't get essential info!", Toast.LENGTH_SHORT);
                        System.out.println(e);
                        myToast.show();
                    }

                    PyObject obj = pyObj.callAttr("text_to_event", speechText);
                    PyObject zip = convertObj.callAttr("convert", latitudeTextView, longitTextView);
                    code = zip.toString();
                    String withLoc = speechText + " at " + code;
                    PyObject search = searchObj.callAttr("start_search", withLoc);
                    String link1 = String.valueOf(search.asList().get(0).asList().get(0));
                    String name1 = String.valueOf(search.asList().get(0).asList().get(1));
                    String link2 = String.valueOf(search.asList().get(1).asList().get(0));
                    String name2 = String.valueOf(search.asList().get(1).asList().get(1));
                    String link3 = String.valueOf(search.asList().get(2).asList().get(0));
                    String name3 = String.valueOf(search.asList().get(2).asList().get(1));
                    des = "info 1: " + name1 +" " + link1 + "\n" + "info 2: " + name2 + " " + link2 + "\n" +
                            "info 3: " + name3 + " " + link3;
                    name = String.valueOf(obj.asMap().get("event subject"));
                    System.out.println(name+100);
                    location = String.valueOf(obj.asMap().get("location"));
                    bool = String.valueOf(obj.asMap().get("boolean"));
                    noun_phrase = String.valueOf(obj.asMap().get("noun phrase"));
                    System.out.println(noun_phrase);
//                    eventDuration = Long.parseLong(String.valueOf(obj.asMap().get("duration")));
//                    eventStartTime = (long)Double.parseDouble(String.valueOf(obj.asMap().get("time")));

                    try {
                        eventStartTime = trans(String.valueOf(obj.asMap().get("start date")));
                        eventEndTime = trans(String.valueOf(obj.asMap().get("end date")));

                    } catch (ParseException e) {
                        e.printStackTrace();
                    }
//                calculateEventStartTime();
//                ArrayList<String> events = (ArrayList<String>) calculateValidTime();
                    ArrayList<String> events = new ArrayList<String>();
                    availableOrNot = true;
                    con = false;
                    if (String.valueOf(obj.asMap().get("end date")) == "null") {
                        System.out.println(eventStartTime);
                        System.out.println("this is true");
                        startUnixTime = eventStartTime;
                        endUnixTime = eventStartTime + 4 * 60*60 * 1000;
                        eventStartTime = getStart(1 * 60*60 * 1000);
                        eventEndTime = eventStartTime + 1 * 60*60 * 1000;
                        if (eventStartTime == -1) {
                            availableOrNot = false;
                        } else {
                            writeToCalender();

                        }
                    } else {
                        calculateEventStartTime();
                        events = (ArrayList<String>) calculateValidTime();

                        writeToCalender();
//                    texttoSpeak(events);
                    }
//                writeToCalender();
                    date = new java.text.SimpleDateFormat("MM/dd/yyyy HH:mm:ss").format(new java.util.Date (eventStartTime));
                    System.out.println(date);
                    texttoSpeak(events);
                } else if (out.equals("shopping")) {
                    System.out.println(2);
                    PyObject shoppingOBJ = py.getModule("get_query");
                    PyObject shopping_noun = shoppingOBJ.callAttr("query_for_shopping", speechText);
                    sendMessage(String.valueOf(shopping_noun));
                } else {
                    Context context = getApplicationContext();
                    CharSequence text = "Invalid request, please try again.";
                    int duration = Toast.LENGTH_SHORT;
                    Toast toast = Toast.makeText(context, text, duration);
                    toast.show();
                    System.out.println(3);
                }
            }

            @Override
            public void onPartialResults(Bundle bundle) {

            }

            @Override
            public void onEvent(int i, Bundle bundle) {

            }
        });


//        show_button.setOnClickListener(new View.OnClickListener() {
//            public void onClick(View v) {
//                // Do something in response to button click
//                queryStartDate = extractDateInformation(startDateText.getText().toString());
//                queryEndDate = extractDateInformation(endDateText.getText().toString());
//
//                queryStartTime = extractTimeInformation(startTimeText.getText().toString());
//                queryEndTime = extractTimeInformation(endTimeText.getText().toString());
//
//                eventDuration = Long.parseLong(eventDurationText.getText().toString())*60*1000;
//
//                // convert this information to Unix timestamp
////                try {
//////                    startUnixTime = parseStringToDate(queryStartDate, queryStartTime);
//////                    endUnixTime = parseStringToDate(queryEndDate, queryEndTime);
////                } catch (ParseException e) {
////                }
//
////                System.out.println(startUnixTime);
////                System.out.println(endUnixTime);
//                // in reality, need code to propose a range of time
//                // in pipeline, if is given
//                calculateEventStartTime();
//            }
//        });
//
//        write_button.setOnClickListener(new View.OnClickListener() {
//            public void onClick(View v) {
//                writeToCalender();
//            }
//        });
    }

    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            int result = textToSpeech.setLanguage(Locale.US);
            if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                Log.e("error", "This Language is not supported");
            }
        } else {
            Log.e("error", "Failed to Initialize");
        }
    }
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (textToSpeech != null) {
            textToSpeech.stop();
            textToSpeech.shutdown();
        }
        speechRecognizer.destroy();
    }

    private void texttoSpeak(ArrayList<String> eList) {

        String text = "I successfully schedule " + name + " at " + date;
        System.out.println("noun_phrase" + noun_phrase);
        text += ". I have also added information about " + name + " in notes for your event.";
        if (availableOrNot) {
            if (con) {
                String listString = "";
                for (String name : eList) {
                    listString += name + " ";
                }
                text += " Note, you also have " + listString + "at that time";
            }
        } else {
            text = "There is no available time";
        }
//        if ("".equals(text)) {
//            text = "Please enter some text to speak.";
//        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null, null);
        }
        else {
            textToSpeech.speak(text, TextToSpeech.QUEUE_FLUSH, null);
        }
    }

    private long trans(String formattime) throws ParseException{
        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date d = format.parse(formattime);
//        System.out.println(d.getTime());
        return d.getTime();
    }

    private void checkRecordPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            ActivityCompat.requestPermissions(this,new String[]{Manifest.permission.RECORD_AUDIO},RecordAudioRequestCode);
        }
    }

    private void checkCalendarPermission(int callbackId, String... permissionsId) {
        boolean permissions = true;
        for (String p : permissionsId) {
            permissions = permissions && ContextCompat.checkSelfPermission(this, p) == PackageManager.PERMISSION_GRANTED;
        }

        if (!permissions)
            ActivityCompat.requestPermissions(this, permissionsId, callbackId);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == RecordAudioRequestCode && grantResults.length > 0 ){
            if(grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Permission Granted", Toast.LENGTH_SHORT).show();
            }
        }
        if (requestCode == PERMISSION_ID) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                System.out.println("result");
                getLastLocation();
            }
        }
    }

    private String[] extractDateInformation (String input) {
        String year = input.substring(0,4);
        String month = input.substring(4,6);
        String day = input.substring(6,8);
        return new String[] {year, month, day};
    }

    private String[] extractTimeInformation (String input) {
        String hour = input.substring(0,2);
        String minute = input.substring(2,4);
        return new String[] {hour, minute};
    }

    private long parseStringToDate (String[] date, String[] time) throws ParseException {
        StringBuilder formattedTime = new StringBuilder();

        formattedTime.append(date[0]);
        formattedTime.append("-");
        formattedTime.append(date[1]);
        formattedTime.append("-");
        formattedTime.append(date[2]);
        formattedTime.append(" ");

        formattedTime.append(time[0]);
        formattedTime.append(":");
        formattedTime.append(time[1]);
        formattedTime.append(":");
        formattedTime.append("00");

        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date d = format.parse(formattedTime.toString());
//        System.out.println(d.getTime());
        return d.getTime();
    }

    // Calculate a valid time slot
    // in pipeline, assume proposed (given) range larger than event duration, then just find the earliest time to put the event
    // if no valid, then return -1
    private List<String> calculateValidTime() {
        ArrayList<String> eNames = new ArrayList<String>();
        con = false;
        if (eventList.size() == 0) {
//            return startUnixTime;
            return eNames;
        }
//        if (eventList.size() == 1) {
//            CalendarDataStruct eventOnCalendar = eventList.get(0);
//            // check head and tail
//            if (eventOnCalendar.startTime-startUnixTime>eventDuration) {
//                return startUnixTime;
//            }
//            if (endUnixTime-eventOnCalendar.endTime>eventDuration) {
//                return eventOnCalendar.endTime;
//            }
//            return -1;
//        }
        for (int i = 0; i < eventList.size(); i++) {
            CalendarDataStruct eventOnCalendar = eventList.get(i);
//            if (i == 0) {
//                if (eventOnCalendar.startTime-startUnixTime>eventDuration) {
//                    return startUnixTime;
//                }
//                if (eventList.get(i+1).startTime - eventOnCalendar.endTime > eventDuration) {
//                    return eventOnCalendar.endTime;
//                }
//            } else if (i == eventList.size() - 1) {
//                if (endUnixTime-eventOnCalendar.endTime>eventDuration) {
//                    return eventOnCalendar.endTime;
//                }
//            } else {
//                if (eventList.get(i+1).startTime - eventOnCalendar.endTime > eventDuration) {
//                    return eventOnCalendar.endTime;
//                }
//            }
            if ((eventOnCalendar.startTime >= eventStartTime && eventOnCalendar.startTime <= eventEndTime) ||
                    (eventOnCalendar.endTime >= eventStartTime && eventOnCalendar.endTime <= eventEndTime) ||
                    (eventOnCalendar.startTime >= eventStartTime && eventOnCalendar.endTime <= eventEndTime) ||
                    (eventOnCalendar.startTime <= eventStartTime && eventOnCalendar.endTime >= eventEndTime)){
                eNames.add(eventOnCalendar.eventTitle);
                con = true;
            }
        }
        return eNames;
    }

    private long getAvailable(ArrayList<CalendarDataStruct> eventArray, long dura) {
        ArrayList<String> eNames = new ArrayList<String>();
//        con = false;
        System.out.println(eventArray.size());
        if (eventArray.size() == 0) {
            return startUnixTime;
//            System.out.println("it is zero");
//            return eNames;
        }
        if (eventArray.size() == 1) {
            CalendarDataStruct eventOnCalendar = eventArray.get(0);
            // check head and tail
            System.out.println(eventOnCalendar.startTime-startUnixTime);
            if (eventOnCalendar.startTime-startUnixTime>dura) {
                System.out.println(8);
                return startUnixTime;
            }
            System.out.println(endUnixTime-eventOnCalendar.endTime);
            if (endUnixTime-eventOnCalendar.endTime>dura) {
                System.out.println(9);
                return eventOnCalendar.endTime;
            }
            System.out.println(15);
            return -1;
        }
        for (int i = 0; i < eventArray.size(); i++) {
            CalendarDataStruct eventOnCalendar = eventArray.get(i);
            if (i == 0) {
                if (eventOnCalendar.startTime-startUnixTime>dura) {
                    System.out.println(10);
                    return startUnixTime;
                }
                if (eventArray.get(i+1).startTime - eventOnCalendar.endTime > dura) {
                    System.out.println(11);
                    return eventOnCalendar.endTime;
                }
            } else if (i == eventArray.size() - 1) {
                if (endUnixTime-eventOnCalendar.endTime>=dura) {
                    System.out.println(12);
                    return eventOnCalendar.endTime;
                }
            } else {
                if (eventArray.get(i+1).startTime - eventOnCalendar.endTime >= dura) {
                    System.out.println(13);
                    return eventOnCalendar.endTime;
                }
            }
//            if ((eventOnCalendar.startTime >= eventStartTime && eventOnCalendar.startTime <= eventEndTime) ||
//                    (eventOnCalendar.endTime >= eventStartTime && eventOnCalendar.endTime <= eventEndTime) ||
//                    (eventOnCalendar.startTime >= eventStartTime && eventOnCalendar.endTime <= eventEndTime) ||
//                    (eventOnCalendar.startTime <= eventStartTime && eventOnCalendar.endTime >= eventEndTime)){
//                eNames.add(eventOnCalendar.eventTitle);
//                con = true;
//            }
        }
//        return eNames;
        System.out.println(14);
        return -1;
    }

    private void calculateEventStartTime() {

        long startTimeForCalendar;
        long endTimeForCalendar;
        String eventTitle;

        Uri.Builder eventsUriBuilder = CalendarContract.Instances.CONTENT_URI
                .buildUpon();

        ContentUris.appendId(eventsUriBuilder, (eventStartTime - 4 * 60 * 1000));
        ContentUris.appendId(eventsUriBuilder, (eventEndTime + 4 * 60 * 1000));

        Uri eventsUri = eventsUriBuilder.build();
        Cursor eventCursor = null;

        eventCursor = MainActivity.this.getContentResolver().query(eventsUri, null, null, null, CalendarContract.Instances.DTSTART + " ASC");
        eventList = new ArrayList<CalendarDataStruct>();
        while (eventCursor.moveToNext()){
            eventTitle = eventCursor.getString(eventCursor.getColumnIndex("title"));
            startTimeForCalendar = eventCursor.getLong(eventCursor.getColumnIndex("dtstart"));
            endTimeForCalendar = eventCursor.getLong(eventCursor.getColumnIndex("dtend"));
            CalendarDataStruct item= new CalendarDataStruct(eventTitle, startTimeForCalendar, endTimeForCalendar); //CalenderDataStruct item=new CalenderDataStruct(eventTitle, startTime, endTime, location,week); //
            eventList.add(item);
        }
        System.out.println(eventList);

        eventCursor.close();
//        eventStartTime = calculateValidTime();
//        System.out.println(eventStartTime);

        Date date = new java.util.Date(eventStartTime);
        // the format of date
        SimpleDateFormat sdf = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        // give a timezone reference for formatting (see comment at the bottom)
        String formattedDate = sdf.format(date);
        System.out.println(formattedDate);
//        showSlot.setText(formattedDate);
    }

    private long getStart(long dura) {
        long startTimeForCalendar;
        long endTimeForCalendar;
        String eventTitle;

        Uri.Builder eventsUriBuilder = CalendarContract.Instances.CONTENT_URI
                .buildUpon();
        System.out.println(startUnixTime);
        System.out.println(eventStartTime);
        System.out.println(endUnixTime);
        System.out.println(20);
        ContentUris.appendId(eventsUriBuilder, startUnixTime);
        ContentUris.appendId(eventsUriBuilder, endUnixTime);

        Uri eventsUri = eventsUriBuilder.build();
        Cursor eventCursor = null;

        eventCursor = MainActivity.this.getContentResolver().query(eventsUri, null, null, null, CalendarContract.Instances.DTSTART + " ASC");
        ArrayList<CalendarDataStruct> allEvents = new ArrayList<CalendarDataStruct>();
        while (eventCursor.moveToNext()){
            eventTitle = eventCursor.getString(eventCursor.getColumnIndex("title"));
            startTimeForCalendar = eventCursor.getLong(eventCursor.getColumnIndex("dtstart"));
            endTimeForCalendar = eventCursor.getLong(eventCursor.getColumnIndex("dtend"));
            CalendarDataStruct item= new CalendarDataStruct(eventTitle, startTimeForCalendar, endTimeForCalendar); //CalenderDataStruct item=new CalenderDataStruct(eventTitle, startTime, endTime, location,week); //
            allEvents.add(item);
        }
        System.out.println(allEvents);
        eventCursor.close();
//        eventStartTime = calculateValidTime();
//        System.out.println(eventStartTime);
        long avaStart = getAvailable(allEvents, dura);
        return avaStart;
//        Date date = new java.util.Date(eventStartTime);
//        // the format of date
//        SimpleDateFormat sdf = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
//        // give a timezone reference for formatting (see comment at the bottom)
//        String formattedDate = sdf.format(date);
//        System.out.println(formattedDate);
//        showSlot.setText(formattedDate);
    }

    private void writeToCalender() {
        System.out.println("final start time is: " + eventStartTime);
//        long eventEndTime = eventStartTime + eventDuration;
        System.out.println("final end time is: " + eventEndTime);
        if (location.equals("geographic info of user's device")) {
            location = code;
        }
        final ContentValues event = new ContentValues();
        event.put(CalendarContract.Events.CALENDAR_ID, 1);
        event.put(CalendarContract.Events.DTSTART, eventStartTime);
        event.put(CalendarContract.Events.DTEND, eventEndTime);
        event.put(CalendarContract.Events.TITLE, name);
        event.put(CalendarContract.Events.DESCRIPTION, des);
        event.put(CalendarContract.Events.EVENT_LOCATION, location);

        String timeZone = TimeZone.getDefault().getID();
        event.put(CalendarContract.Events.EVENT_TIMEZONE, timeZone);

        Uri baseUri;
        if (Build.VERSION.SDK_INT >= 8) {
            baseUri = Uri.parse("content://com.android.calendar/events");
        } else {
            baseUri = Uri.parse("content://calendar/events");
        }
        MainActivity.this.getContentResolver().insert(baseUri, event);
    }


    @SuppressLint("MissingPermission")
    private void getLastLocation() {
        // check if permissions are given
        if (checkPermissions()) {

            // check if location is enabled
            if (isLocationEnabled()) {

                // getting last
                // location from
                // FusedLocationClient
                // object
                mFusedLocationClient.getLastLocation().addOnCompleteListener(new OnCompleteListener<Location>() {
                    @Override
                    public void onComplete(@NonNull Task<Location> task) {
                        Location location = task.getResult();
                        if (location == null) {
                            requestNewLocationData();
                        } else {
                            latitudeTextView = location.getLatitude();
                            longitTextView = location.getLongitude();
                            System.out.println("Longitude: " + longitTextView);
                            System.out.println("lat" + latitudeTextView);
                        }
                    }
                });
            } else {
                Toast.makeText(this, "Please turn on" + " your location...", Toast.LENGTH_LONG).show();
                Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
                startActivity(intent);
            }
        } else {
            // if permissions aren't available,
            // request for permissions
            requestPermissions();
        }
//        System.out.println(latitudeTextView + 666);
    }

    @SuppressLint("MissingPermission")
    private void requestNewLocationData() {

        // Initializing LocationRequest
        // object with appropriate methods
        LocationRequest mLocationRequest = new LocationRequest();
        mLocationRequest.setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY);
        mLocationRequest.setInterval(5);
        mLocationRequest.setFastestInterval(0);
        mLocationRequest.setNumUpdates(1);

        // setting LocationRequest
        // on FusedLocationClient
        mFusedLocationClient = LocationServices.getFusedLocationProviderClient(this);
        mFusedLocationClient.requestLocationUpdates(mLocationRequest, mLocationCallback, Looper.myLooper());
    }

    private LocationCallback mLocationCallback = new LocationCallback() {

        @Override
        public void onLocationResult(LocationResult locationResult) {
            Location mLastLocation = locationResult.getLastLocation();
//            latitudeTextView.setText("Latitude: " + mLastLocation.getLatitude() + "");
//            longitTextView.setText("Longitude: " + mLastLocation.getLongitude() + "");
//            System.out.println("Longitude: " + mLastLocation.getLongitude() + "");
//            System.out.println("Longitude: ");
        }
    };

    // method to check for permissions
    private boolean checkPermissions() {
        return ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED;

        // If we want background location
        // on Android 10.0 and higher,
        // use:
        // ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_BACKGROUND_LOCATION) == PackageManager.PERMISSION_GRANTED
    }

    // method to request for permissions
    private void requestPermissions() {
        ActivityCompat.requestPermissions(this, new String[]{
                Manifest.permission.ACCESS_COARSE_LOCATION,
                Manifest.permission.ACCESS_FINE_LOCATION}, PERMISSION_ID);
    }

    // method to check
    // if location is enabled
    private boolean isLocationEnabled() {
        LocationManager locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) || locationManager.isProviderEnabled(LocationManager.NETWORK_PROVIDER);
    }

    @Override
    public void onResume() {
        super.onResume();
        if (checkPermissions()) {
            System.out.println("resume");
            getLastLocation();
        }
    }

    public void sendMessage(String message) {
        Intent intent = new Intent(this, Shopping.class);
        intent.putExtra(EXTRA_MESSAGE, message);
        startActivity(intent);
    }

}