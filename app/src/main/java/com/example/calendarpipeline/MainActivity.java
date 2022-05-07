package com.example.calendarpipeline;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.CalendarContract;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.text.InputType;
import android.text.format.Time;
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
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;
import java.util.Map;
import java.util.TimeZone;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends AppCompatActivity {

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
    private long startUnixTime;
    private long endUnixTime;
    private long eventDuration;
    private long eventStartTime;

    private ArrayList<CalendarDataStruct> eventList;

    private SpeechRecognizer speechRecognizer;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            checkRecordPermission();
        }

        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_CALENDAR) != PackageManager.PERMISSION_GRANTED) {
            checkCalendarPermission(callbackId, Manifest.permission.READ_CALENDAR, Manifest.permission.WRITE_CALENDAR);
        }

        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

        startDateText = (EditText)findViewById(R.id.start_date_input);
        startTimeText = (EditText)findViewById(R.id.start_time_input);
        endDateText = (EditText)findViewById(R.id.end_date_input);
        endTimeText = (EditText)findViewById(R.id.end_time_input);
        eventNameText = (EditText)findViewById(R.id.event_name_input);
        eventDurationText = (EditText)findViewById(R.id.event_duration_input);
        showSlot = (TextView)findViewById(R.id.time_slot);

        startDateText.setRawInputType(InputType.TYPE_CLASS_NUMBER);
        startTimeText.setRawInputType(InputType.TYPE_CLASS_NUMBER);
        endDateText.setRawInputType(InputType.TYPE_CLASS_NUMBER);
        endTimeText.setRawInputType(InputType.TYPE_CLASS_NUMBER);

        show_button = (Button)findViewById(R.id.show_button);
        write_button = (Button)findViewById((R.id.write_button));
        micButton = findViewById(R.id.mic_button);

        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        final Intent speechRecognizerIntent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        speechRecognizerIntent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());


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
                String speechText = data.toString();
                Python py = Python.getInstance();
                PyObject pyObj = py.getModule("SpeechConvert");
                PyObject obj = pyObj.callAttr("main", speechText);
                name = String.valueOf(obj.asMap().get("event subject"));
                eventDuration = Long.parseLong(String.valueOf(obj.asMap().get("duration")));
                eventStartTime = (long)Double.parseDouble(String.valueOf(obj.asMap().get("time")));
                startUnixTime = eventStartTime;
                endUnixTime = eventStartTime + 4 * 60 * 1000;
//                System.out.println(name);
//                System.out.println(eventDuration);
//                System.out.println(eventStartTime);
                calculateEventStartTime();
                writeToCalender();
            }

            @Override
            public void onPartialResults(Bundle bundle) {

            }

            @Override
            public void onEvent(int i, Bundle bundle) {

            }
        });


        show_button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                // Do something in response to button click
                queryStartDate = extractDateInformation(startDateText.getText().toString());
                queryEndDate = extractDateInformation(endDateText.getText().toString());

                queryStartTime = extractTimeInformation(startTimeText.getText().toString());
                queryEndTime = extractTimeInformation(endTimeText.getText().toString());

                eventDuration = Long.parseLong(eventDurationText.getText().toString())*60*1000;

                // convert this information to Unix timestamp
                try {
                    startUnixTime = parseStringToDate(queryStartDate, queryStartTime);
                    endUnixTime = parseStringToDate(queryEndDate, queryEndTime);
                } catch (ParseException e) {
                }

//                System.out.println(startUnixTime);
//                System.out.println(endUnixTime);
                // in reality, need code to propose a range of time
                // in pipeline, if is given
                calculateEventStartTime();
            }
        });

        write_button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                writeToCalender();
            }
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        speechRecognizer.destroy();
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
            if(grantResults[0] == PackageManager.PERMISSION_GRANTED)
                Toast.makeText(this,"Permission Granted",Toast.LENGTH_SHORT).show();
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
    private long calculateValidTime() {
        if (eventList.size() == 0) {
            return startUnixTime;
        }
        if (eventList.size() == 1) {
            CalendarDataStruct eventOnCalendar = eventList.get(0);
            // check head and tail
            if (eventOnCalendar.startTime-startUnixTime>eventDuration) {
                return startUnixTime;
            }
            if (endUnixTime-eventOnCalendar.endTime>eventDuration) {
                return eventOnCalendar.endTime;
            }
            return -1;
        }
        for (int i = 0; i < eventList.size(); i++) {
            CalendarDataStruct eventOnCalendar = eventList.get(i);
            if (i == 0) {
                if (eventOnCalendar.startTime-startUnixTime>eventDuration) {
                    return startUnixTime;
                }
                if (eventList.get(i+1).startTime - eventOnCalendar.endTime > eventDuration) {
                    return eventOnCalendar.endTime;
                }
            } else if (i == eventList.size() - 1) {
                if (endUnixTime-eventOnCalendar.endTime>eventDuration) {
                    return eventOnCalendar.endTime;
                }
            } else {
                if (eventList.get(i+1).startTime - eventOnCalendar.endTime > eventDuration) {
                    return eventOnCalendar.endTime;
                }
            }
        }
        return -1;
    }

    private void calculateEventStartTime() {

        long startTimeForCalendar;
        long endTimeForCalendar;
        String eventTitle;

        Uri.Builder eventsUriBuilder = CalendarContract.Instances.CONTENT_URI
                .buildUpon();

        ContentUris.appendId(eventsUriBuilder, startUnixTime);
        ContentUris.appendId(eventsUriBuilder, endUnixTime);

        Uri eventsUri = eventsUriBuilder.build();
        Cursor eventCursor = null;
        eventCursor = MainActivity.this.getContentResolver().query(eventsUri, null, null, null, CalendarContract.Instances.DTSTART + " ASC");

        eventList =new ArrayList<CalendarDataStruct>();
        while (eventCursor.moveToNext()){
            eventTitle = eventCursor.getString(eventCursor.getColumnIndex("title"));
            startTimeForCalendar = eventCursor.getLong(eventCursor.getColumnIndex("dtstart"));
            endTimeForCalendar = eventCursor.getLong(eventCursor.getColumnIndex("dtend"));
            CalendarDataStruct item=new CalendarDataStruct(eventTitle, startTimeForCalendar, endTimeForCalendar); //CalenderDataStruct item=new CalenderDataStruct(eventTitle, startTime, endTime, location,week); //
            eventList.add(item);
        }
        System.out.println(eventList);
        eventStartTime = calculateValidTime();
        System.out.println(eventStartTime);

        Date date = new java.util.Date(eventStartTime);
        // the format of date
        SimpleDateFormat sdf = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        // give a timezone reference for formatting (see comment at the bottom)
        String formattedDate = sdf.format(date);
        System.out.println(formattedDate);
        showSlot.setText(formattedDate);
    }

    private void writeToCalender() {
        System.out.println("final start time is: " + eventStartTime);
        long eventEndTime = eventStartTime + eventDuration;
        System.out.println("final end time is: " + eventEndTime);
        final ContentValues event = new ContentValues();
        event.put(CalendarContract.Events.CALENDAR_ID, 1);
        event.put(CalendarContract.Events.DTSTART, eventStartTime);
        event.put(CalendarContract.Events.DTEND, eventEndTime);
        event.put(CalendarContract.Events.TITLE, name);

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
}